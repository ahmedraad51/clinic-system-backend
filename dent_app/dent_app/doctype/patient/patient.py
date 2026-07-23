import frappe
from frappe.model.document import Document
from frappe.utils import getdate, today

class Patient(Document):
    def before_insert(self):
        self.patient_id = self.name

    def validate(self):
        self.calculate_age()
        self.update_statistics()

    def calculate_age(self):
        if self.date_of_birth:
            dob = getdate(self.date_of_birth)
            today_date = getdate(today())
            self.age = (
                today_date.year - dob.year
                - ((today_date.month, today_date.day) < (dob.month, dob.day))
            )

    def update_statistics(self):
        if frappe.db.exists("DocType", "Appointment"):
            self.total_appointments = frappe.db.count(
                "Appointment", {"patient": self.name}
            ) or 0
        else:
            self.total_appointments = 0

        if frappe.db.exists("DocType", "Treatment Plan"):
            self.total_treatments = frappe.db.count(
                "Treatment Plan", {"patient": self.name}
            ) or 0
            remaining = frappe.db.sql(
                "SELECT IFNULL(SUM(remaining_amount), 0) FROM `tabTreatment Plan` WHERE patient = %s",
                self.name
            )
            self.total_remaining = remaining[0][0] if remaining else 0
        else:
            self.total_treatments = 0
            self.total_remaining = 0

        if frappe.db.exists("DocType", "Payment"):
            paid = frappe.db.sql(
                "SELECT IFNULL(SUM(amount), 0) FROM `tabPayment` WHERE patient = %s",
                self.name
            )
            self.total_paid = paid[0][0] if paid else 0
        else:
            self.total_paid = 0