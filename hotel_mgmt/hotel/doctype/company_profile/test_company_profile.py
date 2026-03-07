# Copyright (c) 2025, Sahl and Contributors
# See license.txt

import frappe
from frappe.tests.utils import FrappeTestCase


class TestCompanyProfile(FrappeTestCase):
    def test_customer_created_from_company_profile(self):
        # Create a new Company Profile
        cp = frappe.get_doc(
            {
                "doctype": "Company Profile",
                "company_name": "Test Company",
                "company_type": "Corporate",
                "phone": "123456789",
                "email": "test@example.com",
                "website": "https://example.com",
                "credit_limit": 5000,
                "payment_terms": "Credit 30 Days",
            }
        )
        cp.insert()

        # Reload doc so auto-link field is set
        cp.reload()

        # Check that Customer got created
        self.assertTrue(cp.erpnext_customer, "Customer was not linked back")
        customer = frappe.get_doc("Customer", cp.erpnext_customer)

        # Validate fields sync correctly
        self.assertEqual(customer.customer_name, "Test Company")
        self.assertEqual(customer.credit_limit, 5000)
        self.assertEqual(customer.payment_terms, "Credit 30 Days")

        # Check address created
        address = frappe.get_all("Address", filters={"address_title": "Test Company"}, fields=["name"])
        self.assertTrue(address, "Address not created for Company Profile")
