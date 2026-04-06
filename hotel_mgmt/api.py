import frappe
from frappe import _
from frappe.utils import add_days, getdate, now_datetime, nowdate

from hotel_mgmt.utils import create_housekeeping, set_room_fields


# ---------- Actions callable from UI ----------
@frappe.whitelist()
def check_in(reservation: str):
    frappe.has_permission("Reservation", "write", reservation, throw=True)
    res = frappe.get_doc("Reservation", reservation)

    if res.status != "Confirmed":
        frappe.throw(_("Reservation must be Confirmed to check in. Current status: {0}").format(res.status))

    # Uses db_set to bypass controller save — room update and housekeeping
    # creation are handled here directly because after_save guards on
    # has_value_changed("status") which db_set does not trigger.
    res.db_set("status", "Checked-in")

    if res.room:
        set_room_fields(
            res.room,
            {
                "status": "Occupied",
                "last_housekeeping_update": now_datetime(),
            },
        )
        create_housekeeping(res.room, "Dirty", "Scheduled", res.check_out_date)

    return "Checked-in"


@frappe.whitelist()
def make_sales_invoice(reservation: str):
    frappe.has_permission("Sales Invoice", "create", throw=True)

    settings = frappe.get_single("Hotel Settings")
    res = frappe.get_doc("Reservation", reservation)
    customer = res.customer or settings.walk_in_customer
    if not customer:
        frappe.throw(_("Set a Customer or configure Walk-in Customer in Hotel Settings."))

    si = frappe.new_doc("Sales Invoice")
    si.customer = customer
    si.set_posting_time = 1

    for d in res.get("reservation_charge") or []:
        si.append(
            "items",
            {
                "item_code": d.item_code,
                "description": d.description,
                "qty": d.qty or 1,
                "rate": d.rate,
                "warehouse": settings.hotel_warehouse,
            },
        )

    if getattr(settings, "default_room_item", None) and res.nightly_rate and res.nights:
        si.append(
            "items",
            {
                "item_code": settings.default_room_item,
                "description": _("Room Nights for {0}").format(res.name),
                "qty": res.nights,
                "rate": res.nightly_rate,
                "warehouse": settings.hotel_warehouse,
            },
        )

    si.insert()
    return si.name


# ---------- Nightly Posting ----------
def post_nightly_charges():
    settings = frappe.get_single("Hotel Settings")
    if not getattr(settings, "default_room_item", None):
        return
    for r in frappe.get_all(
        "Reservation",
        filters={"status": "Checked-in", "docstatus": 1},
        fields=["name", "nightly_rate"],
    ):
        res = frappe.get_doc("Reservation", r.name)
        res.append(
            "reservation_charge",
            {
                "item_code": settings.default_room_item,
                "description": _("Room Night"),
                "qty": 1,
                "rate": res.nightly_rate,
                "amount": res.nightly_rate,
            },
        )
        res.flags.ignore_validate_update_after_submit = True
        res.save()


# ---------- Allotment Release ----------
def release_allotments():
    """Release allotment rooms past release period back to Available."""
    today = getdate(nowdate())

    contracts = frappe.get_all(
        "Hotel Contract",
        filters={"contract_type": "Allotment", "docstatus": 1},
        fields=["name", "release_period", "start_date", "end_date"],
    )

    for c in contracts:
        release_period = c.get("release_period") or 0
        start_date = c.get("start_date")

        if not start_date:
            continue

        release_date = add_days(start_date, -release_period)
        if today < release_date:
            continue

        reservations = frappe.get_all(
            "Reservation",
            filters={
                "contract": c["name"],
                "status": "Confirmed",
                "check_in_date": [">=", today],
            },
            fields=["name", "room"],
        )

        for r in reservations:
            frappe.db.set_value("Reservation", r["name"], "status", "Released")
            if r.get("room"):
                set_room_fields(
                    r["room"],
                    {
                        "status": "Available",
                        "clean_status": "Clean",
                        "last_housekeeping_update": now_datetime(),
                    },
                )


# ---------- Auto Expire Hotel Contracts ----------
def expire_hotel_contracts():
    """Expire contracts past their end date."""
    today = getdate(nowdate())

    contracts = frappe.get_all(
        "Hotel Contract",
        filters={"workflow_state": "Active", "docstatus": 1},
        fields=["name", "end_date"],
    )

    for c in contracts:
        if c.get("end_date") and getdate(c["end_date"]) <= today:
            frappe.db.set_value(
                "Hotel Contract",
                c["name"],
                {
                    "workflow_state": "Expired",
                    "status": "Expired",
                },
            )
