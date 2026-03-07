# Copyright (c) 2025, Sahl and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document


class CompanyProfile(Document):
    def after_insert(self):
        self.sync_customer()

    def on_update(self):
        self.sync_customer()

    def sync_customer(self):
        # Check if customer already exists
        existing_customer = frappe.db.exists("Customer", {"customer_name": self.company_name})
        if existing_customer:
            customer = frappe.get_doc("Customer", existing_customer)
        else:
            customer = frappe.new_doc("Customer")
            customer.customer_name = self.company_name
            customer.customer_type = "Company"
            customer.customer_group = "All Customer Groups"  # adjust if needed
            customer.territory = "All Territories"

        # Sync financial info
        customer.payment_terms = self.payment_terms or None
        customer.credit_limit = self.credit_limit or 0

        # Sync tax info
        customer.tax_id = self.tax_id or None
        customer.tax_category = getattr(self, "tax_category", None)
        customer.tax_withholding_category = getattr(self, "tax_withholding_category", None)

        # Insert or update customer
        if existing_customer:
            customer.save(ignore_permissions=True)
        else:
            customer.insert(ignore_permissions=True)

        # Link addresses
        if hasattr(self, "addresses") and self.addresses:
            for addr_link in self.addresses:
                if addr_link.link_doctype == "Address" and addr_link.link_name:
                    address_doc = frappe.get_doc("Address", addr_link.link_name)

                    # Add link to customer if not already linked
                    if not any(
                        l.link_doctype == "Customer" and l.link_name == customer.name
                        for l in address_doc.links
                    ):
                        address_doc.append("links", {"link_doctype": "Customer", "link_name": customer.name})
                        address_doc.save(ignore_permissions=True)

                    # Set first address as primary
                    if not customer.customer_primary_address:
                        customer.customer_primary_address = address_doc.name
                        customer.save(ignore_permissions=True)

        frappe.msgprint(
            f"✅ Customer <b>{customer.name}</b> created/updated and linked with addresses + tax info."
        )
