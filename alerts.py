import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

class SecurityAlerts:
    def __init__(self, email_sender=None, email_password=None, email_receiver=None):
        self.email_sender = email_sender
        self.email_password = email_password
        self.email_receiver = email_receiver

    def send_alert(self, message):
        # Console Alert
        print(f"ALERT: {message}")

        # Email Alert
        if self.email_sender and self.email_password and self.email_receiver:
            try:
                msg = MIMEMultipart()
                msg['From'] = self.email_sender
                msg['To'] = self.email_receiver
                msg['Subject'] = "Security Alert"
                msg.attach(MIMEText(message, 'plain'))

                with smtplib.SMTP('smtp.gmail.com', 587) as server:
                    server.starttls()
                    server.login(self.email_sender, self.email_password)
                    server.sendmail(self.email_sender, self.email_receiver, msg.as_string())

                print("Email alert sent successfully.")
            except Exception as e:
                print(f"Failed to send email alert: {e}")
