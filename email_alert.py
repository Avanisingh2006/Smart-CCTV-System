import os
import smtplib

from email.message import EmailMessage
from dotenv import load_dotenv

load_dotenv()

EMAIL_ADDRESS = os.getenv("EMAIL_ADDRESS")
EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD")
RECEIVER_EMAIL = os.getenv("RECEIVER_EMAIL")


def send_email(image_path):
    try:

        msg = EmailMessage()

        msg["Subject"] = "🚨 Smart CCTV Alert"
        msg["From"] = EMAIL_ADDRESS
        msg["To"] = RECEIVER_EMAIL

        msg.set_content(
            "Intruder detected!\n\n"
            "A person entered the restricted zone.\n"
            "Screenshot attached."
        )

        with open(image_path, "rb") as f:
            img_data = f.read()

        msg.add_attachment(
            img_data,
            maintype="image",
            subtype="jpeg",
            filename=os.path.basename(image_path)
        )

        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
            smtp.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
            smtp.send_message(msg)

        print("✅ Email sent!")

    except Exception as e:
        print("❌ Email Error:", e)
        