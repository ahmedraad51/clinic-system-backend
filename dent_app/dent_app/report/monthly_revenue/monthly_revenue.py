import frappe


def execute(filters=None):
    columns = [
        {"label": "Month", "fieldname": "month", "fieldtype": "Data", "width": 150},
        {"label": "Total Revenue", "fieldname": "total_revenue", "fieldtype": "Currency", "width": 200},
        {"label": "Payment Count", "fieldname": "payment_count", "fieldtype": "Int", "width": 150}
    ]

    data = frappe.db.sql(
        """
        SELECT
            DATE_FORMAT(payment_date, '%%Y-%%m') AS month,
            SUM(amount) AS total_revenue,
            COUNT(*) AS payment_count
        FROM `tabPayment`
        GROUP BY DATE_FORMAT(payment_date, '%%Y-%%m')
        ORDER BY month DESC
        """,
        as_dict=True
    )

    return columns, data