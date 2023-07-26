import os
from application import celery
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart


@celery.task()
def send_email(email, made_verification_token):
    email_sender = "sumeetchoudhary777@gmail.com"
    email_sender_password = os.environ.get("EMAIL_PASSWORD")
    email_receiver = email

    html = f"""
    <html>
      <body>
        <h1><a href='http://127.0.0.1:5000/verification?token={made_verification_token}'>Your verification link</a></h1>
      </body>
    </html>
    """

    subject = "Dear user"
    em = MIMEMultipart("alternative")
    em["FROM"] = email_sender
    em["TO"] = email_receiver
    em["SUBJECT"] = subject

    em_link = MIMEText(html, 'html')
    em.attach(em_link)
    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
        smtp.login(email_sender, email_sender_password)
        smtp.sendmail(email_sender, email_receiver, em.as_string())
