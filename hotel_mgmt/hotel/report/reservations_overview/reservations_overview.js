// Copyright (c) 2026, Sahl and contributors
// For license information, please see license.txt

frappe.query_reports["Reservations Overview"] = {

    filters: [
        {
            fieldname: "status",
            label: "Status",
            fieldtype: "Select",
            options: "\nDraft\nPending\nConfirmed\nChecked-in\nChecked-out\nReleased\nRejected\nCancelled"
        },
        {
            fieldname: "from_date",
            label: "From Date",
            fieldtype: "Date"
        },
        {
            fieldname: "to_date",
            label: "To Date",
            fieldtype: "Date"
        },
        {
            fieldname: "check_in_date",
            label: "Check in Date",
            fieldtype: "Date"
        },
        {
            fieldname: "check_out_date",
            label: "Check out Date",
            fieldtype: "Date"
        },
        {
            fieldname: "room",
            label: "Room",
            fieldtype: "Link",
            options: "Room"
        },
        {
            fieldname: "room_type",
            label: "Room Type",
            fieldtype: "Link",
            options: "Room Type"
        },
        {
            fieldname: "customer",
            label: "Customer",
            fieldtype: "Link",
            options: "Customer"
        },
        {
            fieldname: "primary_guest",
            label: "Primary Guest",
            fieldtype: "Data"
        }
    ],

    onload: function () {
        frappe.msgprint("📋 Reservations Overview Loaded");
    },

    formatter: function (value, row, column, data, default_formatter) {

        value = default_formatter(value, row, column, data);

        // =====================
        // STATUS BADGES
        // =====================
        if (column.fieldname === "status") {

            const styles = {
                "Draft": "background:#e5e7eb;color:#374151;",
                "Pending": "background:#fef3c7;color:#92400e;",
                "Confirmed": "background:#dbeafe;color:#1e40af;",
                "Checked-in": "background:#dcfce7;color:#166534;",
                "Checked-out": "background:#e0f2fe;color:#075985;",
                "Released": "background:#f3f4f6;color:#111827;",
                "Rejected": "background:#fee2e2;color:#b91c1c;",
                "Cancelled": "background:#fecaca;color:#7f1d1d;"
            };

            value = `
                <span style="
                    padding:4px 10px;
                    border-radius:20px;
                    font-weight:bold;
                    ${styles[data.status] || ""}
                ">
                    ${data.status || ""}
                </span>
            `;
        }

        if (column.fieldname === "room") {
            if (data.room) {
                value = `<a href="/app/room/${data.room}" style="font-weight:bold;color:#2563eb;">
                            🏨 ${data.room}
                         </a>`;
            }
        }


        if (column.fieldname === "room_type") {
            if (data.room_type) {
                value = `<a href="/app/room-type/${data.room_type}" style="font-weight:bold;color:#2563eb;">
                            ${data.room_type}
                         </a>`;
            }
        }
        // if (column.fieldname === "name") {
        //     value = `<a href="/app/room-type/${data.name}" 
        //                 style="font-weight:bold;color:#2563eb;">
        //                 ${data.name}
        //              </a>`;
        // }

        if (column.fieldname === "customer") {
            if (data.customer) {
                value = `<a href="/app/customer/${data.customer}" style="font-weight:bold;color:#2563eb;">
                            ${data.customer}
                         </a>`;
            }
        }


        if (column.fieldname === "primary_guest") {
            if (data.primary_guest) {
                value = `<span style="
                    background:#f1f5f9;
                    padding:4px 8px;
                    border-radius:8px;
                    font-weight:600;
                ">
                    👤 ${data.primary_guest}
                </span>`;
            } else {
                value = "-";
            }
        }


        if (
            column.fieldname === "check_in_date" ||
            column.fieldname === "check_out_date" ||
            column.fieldname === "from_date" ||
            column.fieldname === "to_date"
        ) {
            if (value) {
                value = `<span style="font-size:12px;color:#374151;">
                            📅 ${value}
                         </span>`;
            }
        }

        return value;
    },

    get_datatable_options: function (options) {

        options.rowHeight = 45;

        options.style = {
            "font-size": "13px"
        };

        return options;
    }
};