# Copyright (c) 2025, Sahl and contributors
# For license information, please see license.txt

import frappe
from frappe import _
from frappe.model.document import Document
from frappe.utils import cint, flt, getdate, now_datetime, nowdate

from hotel_mgmt.utils import create_housekeeping, set_room_fields


class Reservation(Document):
    def validate(self):
        self._validate_dates()
        self._calculate_totals()
        self._sync_workflow_state()

    def after_save(self):
        """Reflect Reservation status into Room and Housekeeping."""
        if not self.room:
            return

        if not self.has_value_changed("status"):
            return

        if self.status == "Checked-in":
            set_room_fields(
                self.room,
                {
                    "status": "Occupied",
                    "last_housekeeping_update": now_datetime(),
                },
            )
            create_housekeeping(self.room, "Dirty", "Scheduled", self.check_out_date)

        elif self.status == "Checked-out":
            create_housekeeping(self.room, "Dirty", "Open", nowdate())
            set_room_fields(
                self.room,
                {
                    "status": "Dirty",
                    "clean_status": "Dirty",
                    "last_housekeeping_update": now_datetime(),
                },
            )

    def on_cancel(self):
        """Free up the room when Reservation is cancelled."""
        if not self.room:
            return

        set_room_fields(
            self.room,
            {
                "status": "Available",
                "clean_status": "Clean",
                "last_housekeeping_update": now_datetime(),
            },
        )

    def _validate_dates(self):
        if self.check_in_date and self.check_out_date:
            ci = getdate(self.check_in_date)
            co = getdate(self.check_out_date)

            if ci < getdate(nowdate()):
                frappe.throw(_("Check-in date cannot be in the past (earlier than today)."))

            self.nights = (co - ci).days
        else:
            self.nights = 0

        if self.nights <= 0:
            frappe.throw(_("Check-out must be after check-in (minimum 1 night)."))

    def _calculate_totals(self):
        self.total_amount = flt(self.nightly_rate) * cint(self.nights)

    def _sync_workflow_state(self):
        if self.workflow_state and self.status != self.workflow_state:
            self.status = self.workflow_state
