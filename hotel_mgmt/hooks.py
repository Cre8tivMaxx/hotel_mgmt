# -------------------------------------------------------------------
# Hotel Management App - hooks.py
# Last Updated: 2025-09-28 04:45 PM
# Author: Sahl (info@sahl-tech.com)
# -------------------------------------------------------------------

# Basic app info
app_name = "hotel_mgmt"
app_title = "Hotel Management"
app_publisher = "Sahl"
app_description = "Hotel management system"
app_email = "info@sahl-tech.com"
app_license = "mit"

required_apps = ["erpnext"]

# Fixtures (exported data you want to keep in Git)
fixtures = [
    "Custom Field",
    "Property Setter",
    "Workspace",
    "Workflow",
    "Client Script",
    "Room Feature",
    'Room',
 'Reservation',
 'rooms',
 'Room Feature',
 'Housekeeping',
 'Room Status Log',
 'Company Profile',
 'Hotel Contract',
 'Hotel Manual',
 'Room Type',
 'Guest Profile',
 'Rate Code',
 'Rate Plan Detail',
 'Meal Plan',
 'Rate Detail',
 'Group Profile',
 'Rooming List',
 'Travel Agent Profile',
 'Guest Preference Item',
 'Restaurant Order',
 'Restaurant Table',
 'Housekeeping Task',
 'Hotel Settings',
    "Room",
]

# Doc Events
doc_events = {
    "Reservation": {
        "validate": "hotel_mgmt.api.reservation_validate",
        "after_save": "hotel_mgmt.api.reservation_on_submit",
        "on_update": "hotel_mgmt.api.reservation_on_update",
        "on_cancel": "hotel_mgmt.api.reservation_on_cancel",
    },
    "Housekeeping": {   # housekeeping sync
        "on_submit": "hotel_mgmt.api.housekeeping_on_submit",
    },
    "Customer": {
        "before_insert": "hotel_mgmt.custom.customer.set_customer_name",
        "validate": "hotel_mgmt.custom.customer.set_customer_name",
        "before_save": "hotel_mgmt.custom.customer.set_customer_name",
    }
}

# Scheduler Events
scheduler_events = {
    "daily": [
        "hotel_mgmt.api.release_allotments",
        "hotel_mgmt.api.expire_hotel_contracts"
    ],
    "hourly": [
        # placeholder for hourly jobs (e.g., sync with channel manager)
    ],
    "weekly": [
        # placeholder for weekly jobs (e.g., housekeeping audit, occupancy report)
    ]
}

# Include JS & CSS
app_include_js = [
    "public/js/guest_profile.js",
    "public/js/hotel.js"
]

app_include_css = ["/assets/hotel_mgmt/css/dashboard.css"]

# Doctype JS (custom listview indicators)
doctype_js = {
    "Room": "public/js/room_indicator.js"
}