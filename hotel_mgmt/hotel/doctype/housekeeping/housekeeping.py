# Copyright (c) 2025, Sahl and contributors
# For license information, please see license.txt

from frappe.model.document import Document
from frappe.utils import now_datetime

from hotel_mgmt.utils import set_room_fields


class Housekeeping(Document):
    def on_submit(self):
        """When a housekeeping record is submitted, update linked Room."""
        if not self.room:
            return

        condition = self.room_condition

        if condition == "Clean":
            set_room_fields(
                self.room,
                {
                    "status": "Available",
                    "clean_status": "Clean",
                    "last_housekeeping_update": now_datetime(),
                },
            )
        else:
            set_room_fields(
                self.room,
                {
                    "status": condition,
                    "clean_status": condition,
                    "last_housekeeping_update": now_datetime(),
                },
            )
