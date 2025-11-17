from flask import Blueprint, render_template, request, flash, redirect, url_for, session
from flask_login import login_user
from datetime import datetime, timedelta
from bson.objectid import ObjectId
from utils import generate_otp, send_otp_email

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    from app import mongo  # Avoid circular import

    if request.method == 'POST':
        action = request.form.get('action')
        email = request.form.get('email').lower()

        user = mongo.db.users.find_one({'email': email})
        if action == 'register':
            if user:
                flash('Email already registered. Please login.', 'error')
                return redirect(url_for('auth.login'))
            mongo.db.users.insert_one({'email': email, 'otp': None, 'otp_expiry': None})
            flash('Registration successful. Please verify via OTP sent to email.', 'success')
            user = mongo.db.users.find_one({'email': email})

        if not user:
            flash('Email not found. Please register first.', 'error')
            return redirect(url_for('auth.login'))

        otp = generate_otp()
        otp_expiry = datetime.utcnow() + timedelta(minutes=5)
        mongo.db.users.update_one(
            {'_id': user['_id']},
            {'$set': {'otp': otp, 'otp_expiry': otp_expiry}}
        )

        send_otp_email(user['email'], otp)
        session['email'] = email
        return redirect(url_for('auth.verify_otp'))

    return render_template('login.html')


@auth_bp.route('/verify_otp', methods=['GET', 'POST'])
def verify_otp():
    from app import mongo
    from app import User

    email = session.get('email')
    if not email:
        return redirect(url_for('auth.login'))

    user = mongo.db.users.find_one({'email': email})
    if request.method == 'POST':
        otp_submitted = request.form.get('otp')
        if user and user['otp'] == otp_submitted and user['otp_expiry'] and user['otp_expiry'] > datetime.utcnow():
            login_user(User(user))
            session.permanent = True
            flash('Logged in successfully', 'success')
            return redirect(url_for('main.index'))
        else:
            flash('Invalid or expired OTP', 'error')

    return render_template('verify_otp.html')
