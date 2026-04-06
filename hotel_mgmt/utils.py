import frappe
from frappe.utils import nowdate


def set_room_fields(room_name: str, values: dict) -> None:
    """Update Room fields safely (dict of field->value)."""
    try:
        frappe.db.set_value("Room", room_name, values)
    except Exception:
        frappe.log_error(f"Failed to update Room {room_name}: {frappe.get_traceback()}")
        raise


def create_housekeeping(
    room: str,
    condition: str = "Dirty",
    status: str = "Open",
    date: str | None = None,
) -> "frappe.Document":
    """Create and insert a Housekeeping record for the given room."""
    hk = frappe.new_doc("Housekeeping")
    hk.room = room
    hk.room_condition = condition
    hk.status = status
    hk.date = date or nowdate()
    hk.insert(ignore_permissions=True)
    return hk
