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
    {
        "dt": "Role",
        "filters": [["name", "in", ["Front Desk"]]],
    },
    "Workflow State",
    "Workflow",
    "Client Script",
    "Room Feature",
    {
        "dt": "DocType",
        "filters": [["name", "in", ["Room"]]],
    },
]

# Doc Events
doc_events = {
    "Reservation": {
        "validate": "hotel_mgmt.api.reservation_validate",
        "on_submit": "hotel_mgmt.api.reservation_on_submit",
        "on_cancel": "hotel_mgmt.api.reservation_on_cancel",
    },
    "Housekeeping": {
        "on_submit": "hotel_mgmt.api.housekeeping_on_submit",
    },
}

# Scheduler Events
scheduler_events = {
    "daily": [
        "hotel_mgmt.api.release_allotments",
        "hotel_mgmt.api.expire_hotel_contracts",
    ],
    "hourly": [],
    "weekly": [],
}

# Include JS & CSS
app_include_js = [
    "public/js/hotel.js",
]

app_include_css = ["/assets/hotel_mgmt/css/dashboard.css"]

# Doctype JS
doctype_js = {
    "Room": "public/js/room_indicator.js",
    "Guest Profile": "public/js/guest_profile.js",
}

export_python_type_annotations = True
