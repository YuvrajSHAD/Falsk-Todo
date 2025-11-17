import os
import random
from flask_mail import Message
import requests

def generate_otp(length=6):
    return ''.join(str(random.randint(0, 9)) for _ in range(length))

def send_otp_email(mail, to_email, otp):
    # Create email message for consistent formatting
    msg = Message('Your OTP for Todo App Login',
                  sender=os.environ['MAIL_USERNAME'],
                  recipients=[to_email])
    msg.body = f'Your OTP code is: {otp}. It expires in 5 minutes.'

    # Prepare Brevo REST API payload
    data = {
        "sender": {"name": "Your App Name", "email": os.environ['MAIL_USERNAME']},
        "to": [{"email": to_email}],
        "subject": msg.subject,
        "textContent": msg.body,
    }
    headers = {
        "api-key": os.environ['SENDINBLUE_API_KEY'],
        "Content-Type": "application/json",
        "Accept": "application/json"
    }

    # Send email via Brevo API
    response = requests.post("https://api.sendinblue.com/v3/smtp/email",
                             json=data,
                             headers=headers)
    response.raise_for_status()
