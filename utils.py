import random
from flask_mail import Message
from itsdangerous import URLSafeTimedSerializer as Serializer
from flask import current_app as app

def generate_otp(length=6):
    return ''.join(str(random.randint(0, 9)) for _ in range(length))

def send_otp_email(mail, to_email, otp):
    msg = Message('Your OTP for Todo App Login',
                  sender=app.config['MAIL_USERNAME'],
                  recipients=[to_email])
    msg.body = f'Your OTP code is: {otp}. It expires in 5 minutes.'
    mail.send(msg)

def create_token(user_id, expires_sec):
    s = Serializer(app.config['SECRET_KEY'], expires_sec)
    return s.dumps({'user_id': user_id}).decode('utf-8')

def verify_token(token):
    s = Serializer(app.config['SECRET_KEY'])
    try:
        user_id = s.loads(token)['user_id']
    except Exception:
        return None
    return user_id
