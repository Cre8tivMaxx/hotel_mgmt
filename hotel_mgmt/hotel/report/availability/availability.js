// Copyright (c) 2025, Sahl and contributors
// For license information, please see license.txt

frappe.query_reports["Availability"] = {
filters: [
    {
      fieldname: "start_date",
      label: "Start Date",
      fieldtype: "Date",
      default: frappe.datetime.get_today(),
      reqd: 1
    },
    {
      fieldname: "days",
      label: "Days",
      fieldtype: "Int",
      default: 7,
      reqd: 1
    }
  ]
};
