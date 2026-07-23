import frappe
from frappe.model.document import Document


class ClinicSettings(Document):

    def validate(self):
        if self.opening_time and self.closing_time:
            if self.opening_time >= self.closing_time:
                frappe.throw("Closing Time must be after Opening Time.")