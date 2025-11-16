from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from datetime import datetime

db = SQLAlchemy()

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    otp = db.Column(db.String(6), nullable=True)     # Store current OTP
    otp_expiry = db.Column(db.DateTime, nullable=True)
    tasks = db.relationship('Task', backref='user', lazy=True)
    
class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    content = db.Column(db.Text, nullable=False)
    done = db.Column(db.Boolean, default=False)
    pos_x = db.Column(db.Float, default=0.0)  # X position on notebook page
    pos_y = db.Column(db.Float, default=0.0)  # Y position on notebook page
    page = db.Column(db.Integer, default=1)   # 1 or 2 for notebook page
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
