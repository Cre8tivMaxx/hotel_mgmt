# Copyright (c) 2025, Sahl and contributors
# For license information, please see license.txt

import frappe

def execute(filters=None):
    columns = [
        {"label": "Room", "fieldname": "room", "fieldtype": "Link", "options": "Room", "width": 180},
        {"label": "Room Type", "fieldname": "room_type", "fieldtype": "Link", "options": "Room Type", "width": 150},
        {"label": "Status", "fieldname": "status", "fieldtype": "Data", "width": 120},
    ]

    # pull rooms; if you have a room_number field, you can order by it
    rooms = frappe.get_all(
        "Room",
        fields=["name as room", "room_type", "status"],
        order_by="room_number asc, name asc"
    )

    data = list(rooms)
    return columns, data


