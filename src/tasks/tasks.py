import smtplib
from email.mime.text import MIMEText

from celery import shared_task
from pydantic import EmailStr

from src.config import settings
from src.tasks.celery_app import celery_instance


@celery_instance.task
def send_email_with_activation_key(email:EmailStr, activation_key:str):
    subject = "Your Activation Key"
    body = f"""
        <html>
            <body>
                <h2>Welcome to Proxy Service!</h2>
                <p>Your activation key: <b>{activation_key}</b></p>
            </body>
        </html>
        """

    msg = MIMEText(body, "html")
    msg["Subject"] = subject
    msg["From"] = "proxy_service777@mail.ru"
    msg["To"] = email

    with smtplib.SMTP(settings.SMTP_HOST, settings.SMTP_PORT) as server:
        server.starttls()
        server.login(settings.SMTP_USERNAME, settings.SMTP_PASSWORD)
        server.send_message(msg)

    return {"status": "sent", "email": email}