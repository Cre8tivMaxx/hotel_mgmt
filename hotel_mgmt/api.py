# ~/frappe-bench/apps/hotel_mgmt/hotel_mgmt/api.py



import frappe
from frappe.utils import cint, flt, nowdate, getdate, add_days
from datetime import timedelta


# ---------- Reservation Validations ----------
def reservation_validate(doc, method=None):
    if doc.check_in_date and doc.check_out_date:
        ci = getdate(doc.check_in_date)
        co = getdate(doc.check_out_date)

        # 1) Prevent past check-in
        if ci < getdate(nowdate()):
            frappe.throw("Check-in date cannot be in the past (earlier than today).")

        # 2) Nights calculation
        doc.nights = (co - ci).days
    else:
        doc.nights = 0

    if doc.nights <= 0:
        frappe.throw("Check-out must be after check-in (minimum 1 night).")

    # 3) Calculate amount
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
    """Called when Reservation is submitted."""
    if not getattr(doc, "room", None):
        return

    if doc.status == "Checked-in":
        _set_room_fields(doc.room, {"occupancy_status": "Occupied"})

    elif doc.status == "Checked-out":
        _set_room_fields(doc.room, {
            "occupancy_status": "Vacant",
            "clean_status": "Dirty"
        })


def reservation_on_cancel(doc, method=None):
    """Free up the room when Reservation is cancelled."""
    if not getattr(doc, "room", None):
        return

    _set_room_fields(doc.room, {
        "occupancy_status": "Vacant",
        "clean_status": "Clean"
    })


def reservation_on_update(doc, method=None):
    """Keep Reservation fields in sync."""
    # Nights consistency
    if doc.check_in_date and doc.check_out_date:
        ci = getdate(doc.check_in_date)
        co = getdate(doc.check_out_date)
        nights = (co - ci).days
        if nights <= 0:
            frappe.throw("Check-out must be after check-in (minimum 1 night).")
        if nights != doc.nights:
            doc.nights = nights

    # Total amount consistency
    if doc.nightly_rate and doc.nights:
        doc.total_amount = flt(doc.nightly_rate) * cint(doc.nights)

    # Workflow sync
    if doc.workflow_state and doc.status != doc.workflow_state:
        doc.status = doc.workflow_state


# ---------- Group Defaults ----------
@frappe.whitelist()
def get_group_defaults(group_profile: str):
    gp = frappe.db.get_value(
        "Group Profile",
        group_profile,
        ["arrival_date", "departure_date", "rate_code", "meal_plan"],
        as_dict=True
    ) or {}
    return {
        "arrival_date": gp.get("arrival_date"),
        "departure_date": gp.get("departure_date"),
        "default_rate": _rate_from_code(gp.get("rate_code")),
        "meal_plan": gp.get("meal_plan")
    }


def _rate_from_code(rate_code: str):
    if not rate_code:
        return None
    return frappe.db.get_value("Rate Code", rate_code, "base_rate") \
        if frappe.db.exists("Rate Code", rate_code) else None


# ---------- Housekeeping ----------
def housekeeping_on_submit(doc, method=None):
    if getattr(doc, "task_type", "") == "Clean" and doc.room:
        frappe.db.set_value("Room", doc.room, "clean_status", "Clean")


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
        frappe.db.set_value("Room", res.room, "occupancy_status", "Occupied")

    # Create housekeeping task for next day
    task = frappe.new_doc("Housekeeping Task")
    task.date = getdate(res.check_in_date) + timedelta(days=1)
    task.shift = "Morning"
    task.room = res.room
    task.task_type = "Clean"
    task.status = "Open"
    task.insert(ignore_permissions=True)
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


import frappe
from frappe.utils import getdate, nowdate, add_days

# ---------- Allotment Release ----------
def release_allotments():
    """Release allotment rooms past release period back to Vacant"""
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
            # release_date = contract start_date - release_period days
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
                    # Mark reservation as Released
                    frappe.db.set_value("Reservation", r["name"], "status", "Released")

                    # Free up the room (if linked)
                    if r.get("room"):
                        frappe.db.set_value("Room", r["room"], "occupancy_status", "Vacant")

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
        if c.get("end_date") and getdate(c["end_date"]) <= today:  # <= instead of <
            frappe.db.set_value("Hotel Contract", c["name"], {
                "workflow_state": "Expired",
                "status": "Expired"
            })

    frappe.db.commit()





# ---------- Hello World OK----------
@frappe.whitelist()
def hello_world():
    frappe.msgprint("Hello from Hotel Management App!")
    return "Hello World OK"

