import frappe


def execute(filters=None):
    columns = [
        {"label": "Treatment Type", "fieldname": "treatment_type", "fieldtype": "Data", "width": 180},
        {"label": "Total Plans", "fieldname": "plan_count", "fieldtype": "Int", "width": 130},
        {"label": "Total Revenue", "fieldname": "total_revenue", "fieldtype": "Currency", "width": 150},
        {"label": "Total Collected", "fieldname": "total_collected", "fieldtype": "Currency", "width": 150}
    ]

    data = frappe.db.sql(
        """
        SELECT
            treatment_type,
            COUNT(*) AS plan_count,
            SUM(total_cost) AS total_revenue,
            SUM(paid_amount) AS total_collected
        FROM `tabTreatment Plan`
        GROUP BY treatment_type
        ORDER BY total_revenue DESC
        """,
        as_dict=True
    )

    return columns, data