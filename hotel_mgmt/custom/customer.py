import frappe

def set_customer_name(doc, method):
    frappe.msgprint("✅ Hook Fired: set_customer_name")

    salutation = doc.salutation or ""
    first = doc.custom_first_name or ""
    last = doc.custom_last_name or ""

    if salutation and last and first:
        doc.customer_name = f"{salutation} {last}, {first}"
    elif last and first:
        doc.customer_name = f"{last}, {first}"
    elif first:
        doc.customer_name = first
    elif last:
        doc.customer_name = last
    else:
        doc.customer_name = "Unnamed"
