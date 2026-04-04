# Copyright (c) 2026, Sahl and contributors
# For license information, please see license.txt

import frappe


def execute(filters=None):
    columns = [
        {
           "fieldname": "name",
           "label": "Reservation ID",
           "fieldtype": "Link",
           "options": "Reservation"
        },
        {
            "fieldname": "status",
            "label": "Status",
            "fieldtype": "Select",
            "options":"\nDraft\nPending\nConfirmed\nChecked-in\nChecked-out\nReleased\nRejected\nCancelled"
        },
        {
            "fieldname": "customer",
            "label": "Customer",
            "fieldtype": "Link",
            "options": "Customer"
        },
        {
            "fieldname": "primary_guest",
            "label": "Primary Guest",
            "fieldtype": "Data"
        },
        {
            "fieldname": "booking_date",
            "label": "Booking Date",
            "fieldtype": "Date"
        },
        {
            "fieldname": "check_in_date",
            "label": "Check in Date",
            "fieldtype": "Date"
        },
        {
            "fieldname": "check_out_date",
            "label": "Check out Date",
            "fieldtype": "Date"
        },
        {
            "fieldname": "nights",
            "label": "Nights",
            "fieldtype": "Int"
        },
        {
            "fieldname": "room",
            "label": "Room",
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
            "fieldname": "nightly_rate",
            "label": "Nightly Rate",
            "fieldtype": "Currency"
        },
        {
            "fieldname": "total_amount",
            "label": "Total Amount",
            "fieldtype": "Currency"
        },
        {
            "fieldname": "guest_profile",
            "label": "Guest Profile",
            "fieldtype": "Link",
            "options": "Guest Profile"
        },
        {
            "fieldname": "company_profile",
            "label": "Company Profile",
            "fieldtype": "Link",
            "options": "Company Profile",
        },
        {
            "fieldname": "group_profile",
            "label": "Group Profile",
            "fieldtype": "Link",
            "options": "Group Profile",
        },
        {
            "fieldname": "agent_profile",
            "label": "Agent Profile",
            "fieldtype": "Link",
            "options": "Travel Agent Profile",
        },
    ]
    filters_dict = {}
    if filters and filters.get("status"):
        filters_dict["status"] = filters.get("status")


    if filters and filters.get("from_date"):
        filters_dict["check_out_date"] = [">=", filters.get("from_date")]

    if filters and filters.get("to_date"):
        filters_dict["check_in_date"] = ["<=", filters.get("to_date")]
    if filters and filters.get("check_in_date"):
        filters_dict["check_in_date"] = filters.get("check_in_date")
    if filters and filters.get("check_out_date"):
        filters_dict["check_out_date"] = filters.get("check_out_date")
    if filters and filters.get("room"):
        filters_dict["room"] = filters.get("room")
    if filters and filters.get("room_type"):
        filters_dict["room_type"] = filters.get("room_type")
    if filters and filters.get("customer"):
        filters_dict["customer"] = filters.get("customer")
    if filters and filters.get("primary_guest"):
        filters_dict["room_type"] = filters.get("primary_guest")




    reservations = frappe.get_all(
        "Reservation",
        filters = filters_dict,
        fields=[
            "name",
            "status",
            "customer",
            "primary_guest",
            "booking_date",
            "check_in_date",
            "check_out_date",
            "nights",
            "room",
            "room_type",
            "nightly_rate",
            "total_amount",
            "guest_profile",
            "company_profile",
            "group_profile",
            "agent_profile",
        ]
    )

    data = reservations
    frappe.logger().info(reservations)
    return columns, data
