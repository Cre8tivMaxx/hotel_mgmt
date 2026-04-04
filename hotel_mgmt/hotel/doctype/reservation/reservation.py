# Copyright (c) 2025, Sahl and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document


class Reservation(Document):
    # begin: auto-generated types
    # This code is auto-generated. Do not modify anything in this block.

    from typing import TYPE_CHECKING

    if TYPE_CHECKING:
        from frappe.types import DF

        from hotel_mgmt.hotel.doctype.reservation_charge.reservation_charge import ReservationCharge

        agent_profile: DF.Link | None
        amended_from: DF.Link | None
        booking_date: DF.Date | None
        check_in_date: DF.Date | None
        check_out_date: DF.Date | None
        company_profile: DF.Link | None
        contract: DF.Link | None
        customer: DF.Link
        group_profile: DF.Link | None
        guest_profile: DF.Link | None
        naming_series: DF.Literal["RES-.YYYY.-.#####"]
        nightly_rate: DF.Currency
        nights: DF.Int
        primary_guest: DF.Data | None
        rate_code: DF.Link | None
        reservation_charge: DF.Table[ReservationCharge]
        room: DF.Link | None
        room_type: DF.Link | None
        status: DF.Literal[
            "",
            "Draft",
            "Pending",
            "Confirmed",
            "Checked-in",
            "Checked-out",
            "Released",
            "Rejected",
            "Cancelled",
        ]
        total_amount: DF.Currency
    # end: auto-generated types

    # Link room with customer after reservation checked in
    def after_insert(self):
        self.set_customer_room()
    
    def on_update(self):
        self.update_customer_room()

    def after_delete(self):
        self.delete_customer_room()


    
    def set_customer_room(self):
        if not self.customer:
            frappe.throw("Customer must be set")

        frappe.db.set_value("Customer", self.customer, "custom_room", self.room)
    
    def delete_customer_room(self):
        if not self.customer:
            frappe.throw("Customer must be set")

        frappe.db.set_value("Customer", self.customer, "custom_room", None)



    def update_customer_room(self):
        if not self.customer:
            frappe.throw("Customer must be set")

        frappe.db.set_value("Customer", self.customer, "custom_room", self.room)
