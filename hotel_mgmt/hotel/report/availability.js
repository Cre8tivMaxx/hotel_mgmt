frappe.query_reports["Availability"] = {
  "filters": [
    {
      fieldname: "room",
      label: __("Room"),
      fieldtype: "Link",
      options: "Room",
      reqd: 0
    },
    {
      fieldname: "start_date",
      label: __("Start Date"),
      fieldtype: "Date",
      default: frappe.datetime.get_today()
    },
    {
      fieldname: "end_date",
      label: __("End Date"),
      fieldtype: "Date",
      default: frappe.datetime.add_days(frappe.datetime.get_today(), 14)
    }
  ]
};

