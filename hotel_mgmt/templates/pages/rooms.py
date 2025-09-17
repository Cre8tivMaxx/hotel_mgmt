import frappe

def get_context(context):
    # Fetch rooms marked as Available
    context.rooms = frappe.get_all(
        "Room",
        filters={"status": "Available"},
        fields=["name", "room_type", "availability_status", "image", "custom_base_rate", "custom_currency"]
    )
    return context
