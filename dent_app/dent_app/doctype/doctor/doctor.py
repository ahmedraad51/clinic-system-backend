import frappe
from frappe.model.document import Document


class Doctor(Document):

    def validate(self):
        self.validate_working_hours()

    def validate_working_hours(self):
        if self.start_time and self.end_time:
            if self.start_time >= self.end_time:
                frappe.throw("End Time must be after Start Time.")