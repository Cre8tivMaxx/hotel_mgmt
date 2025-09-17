frappe.ready(() => {
    const style = document.createElement("style");
    style.innerHTML = `
        /* Banner في الهيدر */
        .page-head {
            background: url("/files/Seahotel.png") no-repeat center center;
            background-size: cover;
            min-height: 200px;
            color: white;
        }

        /* باقي الصفحة يفضل أبيض */
        body, .page-container, .layout-main-section, .desk-container {
            background: white !important;
        }
    `;
    document.head.appendChild(style);
});

