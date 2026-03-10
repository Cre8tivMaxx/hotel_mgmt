# Copyright (c) 2025, Sahl and contributors
# For license information, please see license.txt

# import frappe
from frappe.model.document import Document


class Room(Document):
    # begin: auto-generated types
    # This code is auto-generated. Do not modify anything in this block.

    from typing import TYPE_CHECKING

    if TYPE_CHECKING:
        from frappe.types import DF

        active: DF.Check
        based_on_amenities: DF.Literal[
            "", "Cabana Room", "Villas", "Penthouses", "Homeyunoon Suite", "Presidential Suite"
        ]
        based_on_bed_size_and_number: DF.Literal[
            "",
            "Queen Room",
            "King Room",
            "Twin Room",
            "Double-Double Room",
            "Hollywood Twin Room",
            "Studio Room",
        ]
        based_on_layout: DF.Literal[
            "",
            "Standard Room",
            "Deluxe Room",
            "Joint Room",
            "Connecting Room",
            "Suite Room",
            "Apartment-Style Room",
            "Accessible Room",
        ]
        based_on_occupancy: DF.Literal["", "Single Room", "Double Room", "Triple Room", "Quad Room"]
        based_on_suites: DF.Literal[
            "",
            "Standard Suite",
            "Junior or Mini Suite",
            "Penthouse Suite",
            "Broad Suite",
            "Presidential Suite",
        ]
        building: DF.Literal["", "A", "B", "C", "D", "F"]
        clean_status: DF.Literal[
            "", "Clean", "Dirty", "Pickup", "Inspected", "Out of Service", "Out of Order"
        ]
        description: DF.SmallText | None
        floor: DF.Literal["", "1", "2", "3", "4", "5", "6", "7", "8", "9", "10"]
        image: DF.AttachImage | None
        last_housekeeping_update: DF.Datetime | None
        out_of_order: DF.Check
        out_of_order_reason: DF.SmallText | None
        out_of_service: DF.Check
        out_of_service_reason: DF.SmallText | None
        rate_override: DF.Currency
        room_number: DF.Literal[
            "1",
            "2",
            "3",
            "4",
            "5",
            "6",
            "7",
            "8",
            "9",
            "10",
            "11",
            "12",
            "13",
            "14",
            "15",
            "16",
            "17",
            "18",
            "19",
            "20",
        ]
        room_type: DF.Link | None
        status: DF.Literal[
            "",
            "Available",
            "Occupied",
            "Dirty",
            "Inspected",
            "Pickup",
            "Out of Service",
            "Out of Order",
            "Reserved",
        ]
    # end: auto-generated types
    pass
