// ✅ Custom ListView Colors for Room Doctype

frappe.listview_settings["Room"] = {
    add_fields: ["status"],

    get_indicator: function (doc) {
        if (!doc.status) return [__("No Status"), "gray", "status,=,''"];

        const status = doc.status.trim();

        switch (status) {
            case "Available":
                return [__("Available"), "green", "status,=,Available"];
            case "Occupied":
                return [__("Occupied"), "red", "status,=,Occupied"];
            case "Dirty":
                return [__("Dirty"), "orange", "status,=,Dirty"];
            case "Inspected":
                return [__("Inspected"), "blue", "status,=,Inspected"];
            case "Pickup":
                return [__("Pickup"), "purple", "status,=,Pickup"];
            case "Out of Service":
            case "Out of Order":
                return [__(status), "gray", `status,=,${status}`];
            case "Reserved":
                return [__("Reserved"), "yellow", "status,=,Reserved"];
            default:
                return [__(status), "gray", `status,=,${status}`];
        }
    },
};
