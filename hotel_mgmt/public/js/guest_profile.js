frappe.ui.form.on('Guest Profile', {
    first_name: function(frm) {
        update_full_name(frm);
    },
    last_name: function(frm) {
        update_full_name(frm);
    }
});

function update_full_name(frm) {
    let first_name = frm.doc.first_name || '';
    let last_name = frm.doc.last_name || '';
    
    // Combine first and last name with a space
    let full_name = `${first_name} ${last_name}`.trim();
    
    // Set the value in the full_name field
    frm.set_value('full_name', full_name);
}