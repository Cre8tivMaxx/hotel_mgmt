# Basic app info
app_name = "hotel_mgmt"
app_title = "Hotel Management"
app_publisher = "Sahl"
app_description = "Hotel management system"
app_email = "info@sahl-tech.com"
app_license = "mit"

required_apps = ["erpnext"]

# Fixtures
fixtures = ["Custom Field", "Property Setter"]

# Doc Events
doc_events = {
    "Reservation": {
        "validate": "hotel_mgmt.api.reservation_validate",
        "on_submit": "hotel_mgmt.api.reservation_on_submit",
        "on_update": "hotel_mgmt.api.reservation_on_update",
        "on_cancel": "hotel_mgmt.api.reservation_on_cancel",
    },
    "Housekeeping Task": {
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
    ]
}
