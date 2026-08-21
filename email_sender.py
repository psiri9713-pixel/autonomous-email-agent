import smtplib
import os
from email.message import EmailMessage
from dotenv import load_dotenv

load_dotenv()


def send_email(receiver, subject, body):
    """
    Sends an email using SMTP.
    """

    sender = os.getenv("EMAIL_ADDRESS")
    password = os.getenv("EMAIL_PASSWORD")

    if not sender or not password:
        print("Email credentials are missing!")
        return False

    message = EmailMessage()
    message["From"] = sender
    message["To"] = receiver
    message["Subject"] = subject
    message.set_content(body)

    try:
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
            smtp.login(sender, password)
            smtp.send_message(message)

        print("Email sent successfully!")
        return True

    except Exception as e:
        print("Failed to send email:", e)
        return False


if __name__ == "__main__":
    send_email(
        "psiri9713@gmail.com",
        "Test Email",
        "This is a test email from the Autonomous Email Agent."
    )