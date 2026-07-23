import frappe
from frappe.model.document import Document


class TreatmentPlan(Document):

    def validate(self):
        self.calculate_remaining()

    def calculate_remaining(self):
        total = self.total_cost or 0
        paid = self.paid_amount or 0
        self.remaining_amount = total - paid

        if self.remaining_amount < 0:
            frappe.throw("Paid Amount cannot exceed Total Cost.")

    def on_update(self):
        if self.patient:
            patient_doc = frappe.get_doc("Patient", self.patient)
            patient_doc.save(ignore_permissions=True)