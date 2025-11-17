from flask import Blueprint, render_template, request, flash, redirect, url_for, session, current_app
from flask_login import login_user
from datetime import datetime, timedelta
from models import db, User
from utils import generate_otp, send_otp_email

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        action = request.form.get('action')
        email = request.form.get('email').lower()

        user = User.query.filter_by(email=email).first()

        if action == 'register':
            if user:
                flash('Email already registered. Please login.', 'error')
                return redirect(url_for('auth.login'))
            user = User(email=email)
            db.session.add(user)
            db.session.commit()
            flash('Registration successful. Please verify via OTP sent to email.', 'success')

        if not user:
            flash('Email not found. Please register first.', 'error')
            return redirect(url_for('auth.login'))

        otp = generate_otp()
        otp_expiry = datetime.utcnow() + timedelta(minutes=5)
        user.otp = otp
        user.otp_expiry = otp_expiry
        db.session.commit()

        send_otp_email(current_app.extensions['mail'], user.email, otp)

        session['email'] = email
        return redirect(url_for('auth.verify_otp'))

    return render_template('login.html')

@auth_bp.route('/verify_otp', methods=['GET', 'POST'])
def verify_otp():
    email = session.get('email')
    if not email:
        return redirect(url_for('auth.login'))

    user = User.query.filter_by(email=email).first()
    if request.method == 'POST':
        otp_submitted = request.form.get('otp')
        if user and user.otp == otp_submitted and user.otp_expiry and user.otp_expiry > datetime.utcnow():
            login_user(user)
            session.permanent = True
            flash('Logged in successfully', 'success')
            return redirect(url_for('main.index'))
        else:
            flash('Invalid or expired OTP', 'error')

    return render_template('verify_otp.html')
