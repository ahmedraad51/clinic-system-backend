import frappe


def execute(filters=None):
    columns = [
        {"label": "Patient", "fieldname": "patient", "fieldtype": "Link", "options": "Patient", "width": 150},
        {"label": "Patient Name", "fieldname": "full_name", "fieldtype": "Data", "width": 180},
        {"label": "Treatment Plan", "fieldname": "name", "fieldtype": "Link", "options": "Treatment Plan", "width": 150},
        {"label": "Total Cost", "fieldname": "total_cost", "fieldtype": "Currency", "width": 130},
        {"label": "Paid Amount", "fieldname": "paid_amount", "fieldtype": "Currency", "width": 130},
        {"label": "Remaining", "fieldname": "remaining_amount", "fieldtype": "Currency", "width": 130}
    ]

    data = frappe.db.sql(
        """
        SELECT
            tp.patient,
            p.full_name,
            tp.name,
            tp.total_cost,
            tp.paid_amount,
            tp.remaining_amount
        FROM `tabTreatment Plan` tp
        LEFT JOIN `tabPatient` p ON p.name = tp.patient
        WHERE tp.remaining_amount > 0
        ORDER BY tp.remaining_amount DESC
        """,
        as_dict=True
    )

    return columns, data