import frappe


def create_dashboard():
    # Create Dashboard Charts
    charts = [
        {
            "doctype": "Dashboard Chart",
            "name": "Monthly Revenue Chart",
            "chart_name": "Monthly Revenue Chart",
            "chart_type": "Sum",
            "document_type": "Payment",
            "based_on": "payment_date",
            "value_based_on": "amount",
            "timespan": "Last Year",
            "time_interval": "Monthly",
            "type": "Bar",
            "color": "#5e64ff",
            "is_public": 1
        },
        {
            "doctype": "Dashboard Chart",
            "name": "Appointments Today Chart",
            "chart_name": "Appointments Today Chart",
            "chart_type": "Count",
            "document_type": "Appointment",
            "based_on": "appointment_date",
            "timespan": "This Week",
            "time_interval": "Daily",
            "type": "Line",
            "color": "#28a745",
            "is_public": 1
        },
        {
            "doctype": "Dashboard Chart",
            "name": "Outstanding Balance Chart",
            "chart_name": "Outstanding Balance Chart",
            "chart_type": "Sum",
            "document_type": "Treatment Plan",
            "based_on": "creation",
            "value_based_on": "remaining_amount",
            "timespan": "Last Year",
            "time_interval": "Monthly",
            "type": "Line",
            "color": "#ff5858",
            "is_public": 1
        }
    ]

    for chart in charts:
        if not frappe.db.exists("Dashboard Chart", chart["name"]):
            doc = frappe.get_doc(chart)
            doc.insert(ignore_permissions=True)
            frappe.db.commit()
            print(f"Created chart: {chart['name']}")
        else:
            print(f"Chart already exists: {chart['name']}")

    # Create Dashboard
    if not frappe.db.exists("Dashboard", "Clinic Dashboard"):
        dashboard = frappe.get_doc({
            "doctype": "Dashboard",
            "name": "Clinic Dashboard",
            "dashboard_name": "Clinic Dashboard",
            "is_default": 1,
            "charts": [
                {"doctype": "Dashboard Chart Link", "chart": "Monthly Revenue Chart", "width": "Full"},
                {"doctype": "Dashboard Chart Link", "chart": "Appointments Today Chart", "width": "Half"},
                {"doctype": "Dashboard Chart Link", "chart": "Outstanding Balance Chart", "width": "Half"}
            ]
        })
        dashboard.insert(ignore_permissions=True)
        frappe.db.commit()
        print("Created Clinic Dashboard")
    else:
        print("Dashboard already exists")

def create_workspace():
    if frappe.db.exists("Workspace", "Dental Clinic"):
        print("Workspace already exists")
        return

    workspace = frappe.get_doc({
        "doctype": "Workspace",
        "name": "Dental Clinic",
        "label": "Dental Clinic",
        "module": "Dent App",
        "category": "Modules",
        "is_standard": 1,
        "icon": "fa fa-hospital-o",
        "color": "#5e64ff",
        "links": [
            {"doctype": "Workspace Link", "type": "DocType", "label": "Patient", "link_to": "Patient", "onboard": 1},
            {"doctype": "Workspace Link", "type": "DocType", "label": "Appointment", "link_to": "Appointment", "onboard": 1},
            {"doctype": "Workspace Link", "type": "DocType", "label": "Doctor", "link_to": "Doctor", "onboard": 1},
            {"doctype": "Workspace Link", "type": "DocType", "label": "Treatment Plan", "link_to": "Treatment Plan", "onboard": 1},
            {"doctype": "Workspace Link", "type": "DocType", "label": "Treatment Session", "link_to": "Treatment Session", "onboard": 0},
            {"doctype": "Workspace Link", "type": "DocType", "label": "Payment", "link_to": "Payment", "onboard": 1},
            {"doctype": "Workspace Link", "type": "DocType", "label": "WhatsApp Template", "link_to": "WhatsApp Template", "onboard": 0},
            {"doctype": "Workspace Link", "type": "DocType", "label": "WhatsApp Log", "link_to": "WhatsApp Log", "onboard": 0},
            {"doctype": "Workspace Link", "type": "Single DocType", "label": "Clinic Settings", "link_to": "Clinic Settings", "onboard": 1}
        ]
    })
    workspace.insert(ignore_permissions=True)
    frappe.db.commit()
    print("Created Dental Clinic Workspace")