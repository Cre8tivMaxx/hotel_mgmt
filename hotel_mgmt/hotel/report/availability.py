import frappe
from frappe.utils import getdate

def execute(filters=None):
    filters = filters or {}
    room = filters.get("room")
    start = getdate(filters.get("start_date")) if filters.get("start_date") else None
    end   = getdate(filters.get("end_date"))   if filters.get("end_date")   else None

    columns = [
        {"label": "Room",         "fieldname": "room",          "fieldtype": "Link", "options": "Room", "width": 140},
        {"label": "Check In",     "fieldname": "check_in_date", "fieldtype": "Date",                   "width": 110},
        {"label": "Check Out",    "fieldname": "check_out_date","fieldtype": "Date",                   "width": 110},
        {"label": "Status",       "fieldname": "status",        "fieldtype": "Data",                   "width": 110},
        {"label": "Guest",        "fieldname": "primary_guest", "fieldtype": "Data",                   "width": 180},
        {"label": "Customer",     "fieldname": "customer",      "fieldtype": "Link", "options": "Customer", "width": 160},
        {"label": "Nights",       "fieldname": "nights",        "fieldtype": "Int",                    "width": 70},
        {"label": "Nightly Rate", "fieldname": "nightly_rate",  "fieldtype": "Currency",               "width": 110},
        {"label": "Total",        "fieldname": "total_amount",  "fieldtype": "Currency",               "width": 110},
    ]

    # Build WHERE parts lazily
    where = ["docstatus < 2"]
    args = {}

    if room:
        where.append("room = %(room)s")
        args["room"] = room

    # If a range is given, include any reservation that overlaps the window
    # (start <= check_out) AND (end >= check_in)
    if start and end:
        where.append("check_in_date <= %(end)s AND check_out_date >= %(start)s")
        args["start"] = start
        args["end"] = end
    elif start:
        where.append("check_out_date >= %(start)s")
        args["start"] = start
    elif end:
        where.append("check_in_date <= %(end)s")
        args["end"] = end

    rows = frappe.db.sql(
        f"""
        SELECT
            room,
            check_in_date,
            check_out_date,
            status,
            primary_guest,
            customer,
            nights,
            nightly_rate,
            total_amount
        FROM `tabReservation`
        WHERE {" AND ".join(where)}
        ORDER BY room, check_in_date
        """,
        args,
        as_dict=True,
    )

    return columns, rows

