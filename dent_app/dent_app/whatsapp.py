import frappe
from frappe.utils import now_datetime, add_to_date, getdate


def send_whatsapp_reminder(appointment_name, trigger):
    """Send WhatsApp reminder for an appointment."""

    # Check if WhatsApp is enabled in Clinic Settings
    settings = frappe.get_single("Clinic Settings")
    if not settings.enable_whatsapp:
        return

    # Get active template for this trigger
    template = frappe.db.get_value(
        "WhatsApp Template",
        {"trigger": trigger, "is_active": 1},
        ["name", "message"],
        as_dict=True
    )
    if not template:
        return

    # Get appointment details
    appointment = frappe.get_doc("Appointment", appointment_name)
    patient = frappe.get_doc("Patient", appointment.patient)
    doctor = frappe.get_doc("Doctor", appointment.doctor)

    # Build message from template
    message = template.message
    message = message.replace("{{patient_name}}", patient.full_name or "")
    message = message.replace("{{date}}", str(appointment.appointment_date) or "")
    message = message.replace("{{time}}", str(appointment.appointment_time) or "")
    message = message.replace("{{doctor_name}}", doctor.full_name or "")
    message = message.replace("{{clinic_name}}", settings.clinic_name or "")

    # Log the reminder
    log = frappe.get_doc({
        "doctype": "WhatsApp Log",
        "patient": appointment.patient,
        "appointment": appointment_name,
        "phone_number": patient.phone_number,
        "message": message,
        "status": "Pending",
        "sent_at": now_datetime()
    })
    log.insert(ignore_permissions=True)

    # NOTE: Actual WhatsApp API call goes here
    # For now we mark as Sent (replace with real API integration later)
    log.status = "Sent"
    log.save(ignore_permissions=True)
    frappe.db.commit()


def schedule_reminders():
    """Called by Frappe scheduler — checks appointments and sends reminders."""

    now = now_datetime()

    # 24 hours before
    target_24h = add_to_date(now, hours=24)
    appointments_24h = frappe.db.sql(
        """
        SELECT name FROM `tabAppointment`
        WHERE appointment_date = %s
        AND status IN ('Scheduled', 'Confirmed')
        """,
        getdate(target_24h),
        as_dict=True
    )
    for apt in appointments_24h:
        send_whatsapp_reminder(apt.name, "24 Hours Before")

    # 2 hours before
    target_2h = add_to_date(now, hours=2)
    appointments_2h = frappe.db.sql(
        """
        SELECT name FROM `tabAppointment`
        WHERE appointment_date = %s
        AND status IN ('Scheduled', 'Confirmed')
        """,
        getdate(target_2h),
        as_dict=True
    )
    for apt in appointments_2h:
        send_whatsapp_reminder(apt.name, "2 Hours Before")