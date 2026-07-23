import frappe
from frappe.model.document import Document


class TreatmentSession(Document):

    def validate(self):
        self.sync_treatment_plan_status()

    def sync_treatment_plan_status(self):
        if not self.treatment_plan:
            return

        if self.status == "In Progress":
            plan = frappe.get_doc("Treatment Plan", self.treatment_plan)
            if plan.status == "Planned":
                plan.status = "In Progress"
                plan.save(ignore_permissions=True)

        elif self.status == "Completed":
            all_sessions_done = not frappe.db.exists(
                "Treatment Session",
                {
                    "treatment_plan": self.treatment_plan,
                    "status": ["!=", "Completed"],
                    "name": ["!=", self.name or ""]
                }
            )
            if all_sessions_done:
                plan = frappe.get_doc("Treatment Plan", self.treatment_plan)
                plan.status = "Completed"
                plan.save(ignore_permissions=True)