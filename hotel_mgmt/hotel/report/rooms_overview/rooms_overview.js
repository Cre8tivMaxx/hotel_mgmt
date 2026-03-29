// Copyright (c) 2026, Sahl and contributors
// For license information, please see license.txt

frappe.query_reports["Rooms Overview"] = {


    filters: [
        {
            fieldname: "status",
            label: "Status",
            fieldtype: "Select",
            options: "\nAvailable\nReserved\nOccupied"
        },
        {
            fieldname: "clean_status",
            label: "Clean Status",
            fieldtype: "Select",
            options: "\nClean\nDirty\nPickup\nInspected\nOut of Service\nOut of Order"
        },
        {
            fieldname: "room_number",
            label: "Room Number",
            fieldtype: "Int"
        },
        {
            fieldname: "room_type",
            label: "Room Type",
            fieldtype: "Link",
            options: "Room Type"
        }
    ],


    onload: function(report) {

        frappe.msgprint("🏨 Rooms Overview Loaded");
    },


    formatter: function(value, row, column, data, default_formatter) {

        value = default_formatter(value, row, column, data);


        if (column.fieldname === "status") {

            const styles = {
                "Available": "background:#e6fffa;color:#0f766e;",
                "Occupied": "background:#fee2e2;color:#b91c1c;",
                "Reserved": "background:#fef3c7;color:#92400e;"
            };

            value = `<span style="padding:4px 10px;border-radius:20px;font-weight:bold;${styles[data.status]}">
                        ${data.status}
                     </span>`;
        }


        if (column.fieldname === "clean_status") {

            const icons = {
                "Clean": "✔",
                "Dirty": "🧹",
                "Pickup": "🚪",
                "Inspected": "🔍",
                "Out of Service": "⚙",
                "Out of Order": "⛔"
            };

            value = `<span style="font-weight:bold;">
                        ${icons[data.clean_status] || ""} ${data.clean_status}
                     </span>`;
        }

        if (column.fieldname === "room_number") {

            if (data.room_number) {
                value = `<span style="
                    font-size:14px;
                    font-weight:bold;
                    background:#f1f5f9;
                    padding:5px 10px;
                    border-radius:8px;
                ">
                    🏷 ${data.room_number}
                </span>`;
            } else {
                value = "-";
            }
        }

        if (column.fieldname === "room_type") {
            value = `<a href="/app/room-type/${data.room_type}" 
                        style="font-weight:bold;color:#2563eb;">
                        ${data.room_type}
                     </a>`;
        }
        if (column.fieldname === "name") {
            value = `<a href="/app/room-type/${data.name}" 
                        style="font-weight:bold;color:#2563eb;">
                        ${data.room_type}
                     </a>`;
        }

        return value;
    },


    get_datatable_options(options) {

        options.rowHeight = 45;

        options.style = {
            "font-size": "13px"
        };

        return options;
    }
};