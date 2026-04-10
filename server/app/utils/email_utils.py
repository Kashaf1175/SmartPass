import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from ..core.config import SMTP_SERVER, SMTP_PORT, SMTP_USERNAME, SMTP_PASSWORD, ADMIN_EMAIL

def send_fraud_alert(student_email: str, fraud_score: int, reasons: list):
    """Send email alert to admin when fraud is detected"""
    if not SMTP_USERNAME or not SMTP_PASSWORD:
        print("SMTP credentials not configured, skipping email alert")
        return

    msg = MIMEMultipart()
    msg['From'] = SMTP_USERNAME
    msg['To'] = ADMIN_EMAIL
    msg['Subject'] = f"Fraud Alert: Suspicious Attendance by {student_email}"

    body = f"""
    Fraudulent attendance detected!

    Student: {student_email}
    Fraud Score: {fraud_score}
    Reasons: {', '.join(reasons)}

    Please investigate immediately.
    """
    msg.attach(MIMEText(body, 'plain'))

    try:
        server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
        server.starttls()
        server.login(SMTP_USERNAME, SMTP_PASSWORD)
        text = msg.as_string()
        server.sendmail(SMTP_USERNAME, ADMIN_EMAIL, text)
        server.quit()
        print(f"Fraud alert email sent to {ADMIN_EMAIL}")
    except Exception as e:
        print(f"Failed to send email: {e}")