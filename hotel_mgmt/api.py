# -------------------------------------------------------------------
# Hotel Management App - api.py
# Last Updated: 2025-09-22 03:35 PM (UTC+3)
# Author: Sahl (info@sahl-tech.com)
# -------------------------------------------------------------------

import frappe
from frappe.utils import cint, flt, nowdate, getdate, add_days, now_datetime


# ---------- Reservation Validations ----------
def reservation_validate(doc, method=None):
    if doc.check_in_date and doc.check_out_date:
        ci = getdate(doc.check_in_date)
        co = getdate(doc.check_out_date)

        # Prevent past check-in
        if ci < getdate(nowdate()):
            frappe.throw("Check-in date cannot be in the past (earlier than today).")

        # Nights calculation
        doc.nights = (co - ci).days
    else:
        doc.nights = 0

    if doc.nights <= 0:
        frappe.throw("Check-out must be after check-in (minimum 1 night).")

    # Calculate amount
    doc.total_amount = flt(doc.nightly_rate) * cint(doc.nights)


# ---------- Helper ----------
def _set_room_fields(room_name, values: dict):
    """Update Room fields safely (dict of field->value)."""
    try:
        for f, v in values.items():
            frappe.db.set_value("Room", room_name, f, v)
    except Exception:
        frappe.log_error(f"Failed to update Room {room_name}: {frappe.get_traceback()}")


# ---------- Reservation Events ----------
def reservation_on_submit(doc, method=None):
    """Reflect Reservation into Room and Housekeeping."""
    if not getattr(doc, "room", None):
        return

    if doc.status == "Checked-in":
        # Mark room as occupied
        _set_room_fields(doc.room, {
            "status": "Occupied",
            "last_housekeeping_update": now_datetime()
        })

        # Pre-schedule housekeeping for checkout
        hk = frappe.new_doc("Housekeeping")
        hk.room = doc.room
        hk.room_condition = "Dirty"
        hk.status = "Scheduled"
        hk.date = doc.check_out_date
        hk.insert(ignore_permissions=True)

    elif doc.status == "Checked-out":
        # Create housekeeping record immediately
        hk = frappe.new_doc("Housekeeping")
        hk.room = doc.room
        hk.room_condition = "Dirty"
        hk.status = "Open"
        hk.date = nowdate()
        hk.insert(ignore_permissions=True)

        # Reflect in Room
        _set_room_fields(doc.room, {
            "status": "Dirty",
            "clean_status": "Dirty",
            "last_housekeeping_update": now_datetime()
        })


def reservation_on_cancel(doc, method=None):
    """Free up the room when Reservation is cancelled."""
    if not getattr(doc, "room", None):
        return

    _set_room_fields(doc.room, {
        "status": "Available",
        "clean_status": "Clean",
        "last_housekeeping_update": now_datetime()
    })


def reservation_on_update(doc, method=None):
    """Keep Reservation fields in sync."""
    if doc.check_in_date and doc.check_out_date:
        ci = getdate(doc.check_in_date)
        co = getdate(doc.check_out_date)
        nights = (co - ci).days
        if nights <= 0:
            frappe.throw("Check-out must be after check-in (minimum 1 night).")
        if nights != doc.nights:
            doc.nights = nights

    if doc.nightly_rate and doc.nights:
        doc.total_amount = flt(doc.nightly_rate) * cint(doc.nights)

    if doc.workflow_state and doc.status != doc.workflow_state:
        doc.status = doc.workflow_state


# ---------- Housekeeping Events ----------
def housekeeping_on_submit(doc, method=None):
    """When a housekeeping record is submitted, update linked Room."""
    if not getattr(doc, "room", None):
        return

    condition = doc.room_condition

    if condition == "Clean":
        _set_room_fields(doc.room, {
            "status": "Available",
            "clean_status": "Clean",
            "last_housekeeping_update": now_datetime()
        })
    else:
        _set_room_fields(doc.room, {
            "status": condition,
            "clean_status": condition,
            "last_housekeeping_update": now_datetime()
        })


# ---------- Nightly Posting ----------
def post_nightly_charges():
    settings = frappe.get_single("Hotel Settings")
    if not getattr(settings, "default_room_item", None):
        return
    for r in frappe.get_all("Reservation",
            filters={"status": "Checked-in", "docstatus": 1},
            fields=["name", "nightly_rate"]):
        res = frappe.get_doc("Reservation", r.name)
        res.append("reservation_charge", {
            "item_code": settings.default_room_item,
            "description": "Room Night",
            "qty": 1,
            "rate": res.nightly_rate,
            "amount": res.nightly_rate,
        })
        res.flags.ignore_validate_update_after_submit = True
        res.save()


# ---------- Actions callable from UI ----------
@frappe.whitelist()
def check_in(reservation: str):
    res = frappe.get_doc("Reservation", reservation)
    res.db_set("status", "Checked-in")

    if res.room:
        frappe.db.set_value("Room", res.room, {
            "status": "Occupied",
            "last_housekeeping_update": now_datetime()
        })

        # Pre-schedule housekeeping for checkout date
        hk = frappe.new_doc("Housekeeping")
        hk.room = res.room
        hk.room_condition = "Dirty"
        hk.status = "Scheduled"
        hk.date = res.check_out_date
        hk.insert(ignore_permissions=True)

    return "Checked-in"


@frappe.whitelist()
def make_sales_invoice(reservation: str):
    settings = frappe.get_single("Hotel Settings")
    res = frappe.get_doc("Reservation", reservation)
    customer = res.customer or settings.walk_in_customer
    if not customer:
        frappe.throw("Set a Customer or configure Walk-in Customer in Hotel Settings.")

    si = frappe.new_doc("Sales Invoice")
    si.customer = customer
    si.set_posting_time = 1

    for d in res.get("reservation_charge") or []:
        si.append("items", {
            "item_code": d.item_code,
            "description": d.description,
            "qty": d.qty or 1,
            "rate": d.rate,
            "warehouse": settings.hotel_warehouse
        })

    if getattr(settings, "default_room_item", None) and res.nightly_rate and res.nights:
        si.append("items", {
            "item_code": settings.default_room_item,
            "description": f"Room Nights for {res.name}",
            "qty": res.nights,
            "rate": res.nightly_rate,
            "warehouse": settings.hotel_warehouse
        })

    si.insert()
    return si.name


# ---------- Allotment Release ----------
def release_allotments():
    """Release allotment rooms past release period back to Available"""
    today = getdate(nowdate())

    contracts = frappe.get_all(
        "Hotel Contract",
        filters={"contract_type": "Allotment", "docstatus": 1},
        fields=["name", "release_period", "start_date", "end_date"]
    )

    for c in contracts:
        release_period = c.get("release_period") or 0
        start_date = c.get("start_date")

        if start_date:
            release_date = add_days(start_date, -release_period)

            if today >= release_date:
                reservations = frappe.get_all(
                    "Reservation",
                    filters={
                        "contract": c["name"],
                        "status": "Confirmed",
                        "check_in_date": [">=", today]
                    },
                    fields=["name", "room"]
                )

                for r in reservations:
                    frappe.db.set_value("Reservation", r["name"], "status", "Released")

                    if r.get("room"):
                        frappe.db.set_value("Room", r["room"], {
                            "status": "Available",
                            "clean_status": "Clean",
                            "last_housekeeping_update": now_datetime()
                        })

    frappe.db.commit()


# ---------- Auto Expire Hotel Contracts ----------
def expire_hotel_contracts():
    """Expire contracts past their end date"""
    today = getdate(nowdate())

    contracts = frappe.get_all(
        "Hotel Contract",
        filters={"workflow_state": "Active", "docstatus": 1},
        fields=["name", "end_date"]
    )

    for c in contracts:
        if c.get("end_date") and getdate(c["end_date"]) <= today:
            frappe.db.set_value("Hotel Contract", c["name"], {
                "workflow_state": "Expired",
                "status": "Expired"
            })

    frappe.db.commit()


# ---------- Hello World ----------
@frappe.whitelist()
def hello_world():
    frappe.msgprint("Hello from Hotel Management App!")
    return "Hello World OK"
