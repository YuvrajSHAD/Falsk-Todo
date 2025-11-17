import os
from sib_api_v3_sdk import ApiClient, Configuration
from sib_api_v3_sdk.api import transactional_emails_api
from sib_api_v3_sdk.models import SendSmtpEmail
import random

def generate_otp(length=6):
    return ''.join(str(random.randint(0, 9)) for _ in range(length))

def send_otp_email(to_email, otp):
    config = Configuration()
    config.api_key['api-key'] = os.environ['SENDINBLUE_API_KEY']

    api_instance = transactional_emails_api.TransactionalEmailsApi(ApiClient(config))

    sender_email = os.environ['MAIL_USERNAME']
    send_smtp_email = SendSmtpEmail(
        to=[{"email": to_email}],
        sender={"email": sender_email, "name": "Your App Name"},
        subject="Your OTP Code",
        text_content=f"Your OTP code is: {otp}. It expires in 5 minutes."
    )

    try:
        api_response = api_instance.send_transac_email(send_smtp_email)
    except Exception as e:
        print(f"Error sending email: {e}")
        raise


def create_token(user_id, expires_sec):
    from itsdangerous import URLSafeTimedSerializer as Serializer
    from flask import current_app as app

    s = Serializer(app.config['SECRET_KEY'], expires_sec)
    return s.dumps({'user_id': user_id}).decode('utf-8')


def verify_token(token):
    from itsdangerous import URLSafeTimedSerializer as Serializer
    from flask import current_app as app

    s = Serializer(app.config['SECRET_KEY'])
    try:
        user_id = s.loads(token)['user_id']
    except Exception:
        return None
    return user_id
