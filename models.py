import json
from datetime import datetime
from hashlib import sha256
from time import time
import jwt
from flask_login import UserMixin
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nickname = db.Column(db.String(120), unique=False, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(120), unique=False, nullable=False)
    country = db.Column(db.String(120), unique=False, nullable=True)
    # noifications = db.relationship('Notification', foreign_keys='Notification.user_id', backref='user', lazy='dynamic')
    # last_notification_read_time = db.Column(db.DateTime)

    def check_password(self, password):
        return self.password == sha256(password.encode("utf-8")).hexdigest()

    def set_password(self, new_password):
        self.password = sha256(new_password.encode("utf-8")).hexdigest()

    # def new_notification(self):
    #     last_read_time = self.last_notification_read_time() or datetime(1900, 1, 1)
    #     return Notification.query.filter_by(user_id=self).filter(last_read_time > last_read_time).count()

    def get_reset_password_token(self, expires_in=600):
        return jwt.encode(
            {'reset_password': self.id, 'exp': time() + expires_in}, 'NeverGonnaGiveYouUP',
            algorithm='HS256')

    @staticmethod
    def verify_reset_password_token(token):
        try:
            id = jwt.decode(token, 'NeverGonnaGiveYouUP',
                            algorithms=['HS256'])['reset_password']
        except:
            return
        return User.query.get(id)


class Notification(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    note = db.Column(db.Text, unique=False, nullable=True)
    reminding_time = db.Column(db.DateTime)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    user = db.relationship('User', backref='note', lazy=True)
    payload_json = db.Column(db.Text)

    def get_data(self):
        return json.loads(str(self.payload_json))


class Summary(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120), unique=False, nullable=True)
    text = db.Column(db.Text, unique=False, nullable=True)
    date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    user = db.relationship('User', backref='summary', lazy=True)
