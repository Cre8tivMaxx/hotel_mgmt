frappe.listview_settings["Room"] = {
    formatters: {
        custom_base_rate: function (value, df, doc) {
            let currency = doc.custom_currency || "";
            return `<span style="font-weight:600; color:#444;">
                        ${currency} ${value || ""}
                    </span>`;
        },
    },

    indicator: function (doc) {
        if (doc.status === "Available") {
            return [__("Available"), "green", "status,=,Available"];
        } else if (doc.status === "Occupied") {
            return [__("Occupied"), "orange", "status,=,Occupied"];
        } else if (doc.status === "Dirty") {
            return [__("Dirty"), "red", "status,=,Dirty"];
        } else if (doc.status === "Inspected") {
            return [__("Inspected"), "blue", "status,=,Inspected"];
        } else if (doc.status === "Out of Service") {
            return [__("Out of Service"), "purple", "status,=,Out of Service"];
        } else if (doc.status === "Out of Order") {
            return [__("Out of Order"), "grey", "status,=,Out of Order"];
        } else {
            return [__(doc.status || "Unknown"), "darkgrey", "status,=," + doc.status];
        }
    },
};
