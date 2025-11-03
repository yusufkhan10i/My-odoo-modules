{
    "name": "Hospital Management System",
    "summary": "Manage Patients, Appointments, and Medical Records",
    "description": """
        A comprehensive Hospital Management System to manage patients, appointments, and medical records efficiently.
    """,
    "category": "Healthcare",
    "author": "Yusuf Khan",
    "license": "LGPL-3",
    "version": "18.0.1.1",
    "depends": [
        "mail",
        "product",
        "stock",
        "hr",
        "sale_management",
        "account",
        "website"

    ],
    "data": [
        "security/ir.model.access.csv",
        "data/sequence.xml",
        "views/odoo_playground_views.xml",
        "wizard/cancel_appointment_views.xml",
        "report/patient_report_pdf.xml",
        "views/patient_views.xml",
        "views/patient_readonly_views.xml",
        "views/appointment_views.xml",
        "views/patient_tag_views.xml",
        "views/appointment_line_views.xml",
        "views/account_move_views.xml",
        "views/employee_id_views.xml",
        "views/menu.xml"
    ],
    "installable": True,
    "application": True,
    "auto_install": True,
    "sequence": -10
}
