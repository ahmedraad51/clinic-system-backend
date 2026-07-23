import frappe
from frappe.model.document import Document


class Appointment(Document):

    def before_insert(self):
        self.appointment_number = self.name

    def validate(self):
        self.check_double_booking()

    def check_double_booking(self):
        if not (self.doctor and self.appointment_date and self.appointment_time):
            return

        existing = frappe.db.sql(
            """
            SELECT name FROM `tabAppointment`
            WHERE doctor = %s
            AND appointment_date = %s
            AND appointment_time = %s
            AND name != %s
            AND status NOT IN ('Cancelled', 'No Show')
            """,
            (self.doctor, self.appointment_date, self.appointment_time, self.name or "")
        )

        if existing:
            frappe.throw(
                f"Doctor already has an appointment at this date and time."
            )

    def on_update(self):
        if self.patient:
            patient_doc = frappe.get_doc("Patient", self.patient)
            patient_doc.save(ignore_permissions=True)