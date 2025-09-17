frappe.listview_settings['Room'] = {
    formatters: {
        custom_base_rate: function(value, df, doc) {
            // Show currency + rate together
            let currency = doc.custom_currency || "";
            return `<span style="font-weight:600; color:#444;">
                        ${currency} ${value || ""}
                    </span>`;
        }
    },
    get_indicator: function(doc) {
        if (doc.occupancy_status === "Vacant") {
            return [__("Available"), "green", "occupancy_status,=,Vacant"];
        } else {
            return [__("Occupied"), "red", "occupancy_status,=,Occupied"];
        }
    }
};
