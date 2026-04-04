# Copyright (c) 2026, Sahl and contributors
# For license information, please see license.txt

import frappe

def execute(filters=None):
    columns = [
        {
           "fieldname": "name",
           "label": "Room ID",
           "fieldtype": "Link",
           "options": "Room"
        },
        {
            "fieldname": "room_type",
            "label": "Room Type",
            "fieldtype": "Link",
            "options": "Room Type"
        },
        {
            "fieldname": "room_number",
            "label": "Room Number",
            "fieldtype": "Int"
        },
        {
            "fieldname": "floor",
            "label": "Floor",
            "fieldtype": "Int"
        },
        {
            "fieldname": "status",
            "label": "Status",
            "fieldtype": "Select",
            "options":"\nAvailable\nReserved\nOccupied"
        },
        {
            "fieldname": "clean_status",
            "label": "Clean Status",
            "fieldtype": "Select",
            "options": "\nClean\nDirty\nPickup\nInspected\nOut of Service\nOut of Order"
        },
        {
            "fieldname": "room_type.base_rate",
            "label": "Base Rate",
            "fieldtype": "Currency"
        },
        {
            "fieldname": "room_type.currency",
            "label": "Currency",
            "fieldtype": "Link",
            "options": "Currency"
        },
        {
            "fieldname": "room_type.capacity",
            "label": "Capacity",
            "fieldtype": "Int"
        },
        {
            "fieldname": "last_housekeeping_update",
            "label": "Last Housekeeping Update",
            "fieldtype": "Datetime"
        }
    ]
    filters_dict = {}
    if filters and filters.get("status"):
        filters_dict["status"] = filters.get("status")
    if filters and filters.get("clean_status"):
        filters_dict["clean_status"] = filters.get("clean_status")
    if filters and filters.get("room_number"):
        room_number = str(filters.get("room_number")).zfill(2)
        filters_dict["room_number"] = ["like", f"%{room_number}%"]
    if filters and filters.get("room_type"):
        filters_dict["room_type"] = filters.get("room_type")




    rooms = frappe.get_all(
        "Room",
        filters = filters_dict,
        fields=[
            "name",
            "room_type",
            "room_type.base_rate",
            "floor",
            "room_number",
            "clean_status",
            "status",
            "last_housekeeping_update",
            "room_type.currency",
            "room_type.capacity",

        ]
    )

    data = rooms

    return columns, data
