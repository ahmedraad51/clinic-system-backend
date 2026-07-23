import frappe
from frappe.model.document import Document


class Payment(Document):

    def before_insert(self):
        self.payment_number = self.name

    def validate(self):
        self.validate_amount_against_plan()

    def validate_amount_against_plan(self):
        if not self.treatment_plan:
            return

        plan = frappe.get_doc("Treatment Plan", self.treatment_plan)

        previous_paid = frappe.db.sql(
            """
            SELECT IFNULL(SUM(amount), 0) FROM `tabPayment`
            WHERE treatment_plan = %s AND name != %s
            """,
            (self.treatment_plan, self.name or "")
        )[0][0]

        new_total_paid = previous_paid + (self.amount or 0)

        if new_total_paid > plan.total_cost:
            frappe.throw(
                f"This payment exceeds the remaining balance. "
                f"Treatment Plan total cost is {plan.total_cost}, "
                f"already paid {previous_paid}."
            )

    def on_update(self):
        self.sync_treatment_plan()

    def on_trash(self):
        self.sync_treatment_plan()

    def sync_treatment_plan(self):
        if not self.treatment_plan:
            return

        total_paid = frappe.db.sql(
            """
            SELECT IFNULL(SUM(amount), 0) FROM `tabPayment`
            WHERE treatment_plan = %s
            """,
            self.treatment_plan
        )[0][0]

        plan = frappe.get_doc("Treatment Plan", self.treatment_plan)
        plan.paid_amount = total_paid
        plan.save(ignore_permissions=True)