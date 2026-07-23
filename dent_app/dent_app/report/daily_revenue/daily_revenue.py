import frappe


def execute(filters=None):
    filters = filters or {}
    report_date = filters.get("report_date") or frappe.utils.today()

    columns = [
        {"label": "Metric", "fieldname": "metric", "fieldtype": "Data", "width": 250},
        {"label": "Value", "fieldname": "value", "fieldtype": "Data", "width": 200}
    ]

    total_revenue = frappe.db.sql(
        """
        SELECT IFNULL(SUM(amount), 0) FROM `tabPayment`
        WHERE payment_date = %s
        """,
        report_date
    )[0][0]

    patient_count = frappe.db.sql(
        """
        SELECT COUNT(DISTINCT patient) FROM `tabPayment`
        WHERE payment_date = %s
        """,
        report_date
    )[0][0]

    data = [
        {"metric": "Total Revenue Today", "value": total_revenue},
        {"metric": "Number of Paying Patients Today", "value": patient_count}
    ]

    return columns, data