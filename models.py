from datetime import datetime
from database import db
# import jwt
from flask import current_app

class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    name = db.Column(db.String(120), nullable=False)
    password = db.Column(db.String(120), nullable=False)
    role = db.Column(db.String(80), nullable=False)
    email = db.Column(db.String(120), nullable=False)
    avatar = db.Column(db.String(255), nullable=True)
    token = db.Column(db.String(255), nullable=True)

    def __init__(self, username, name, password, role, email, avatar=None, token=None):
        self.username = username
        self.name = name
        self.password = password
        self.role = role
        self.email = email
        self.avatar = avatar
        self.token = token

    def check_password(self, password):
        return self.password == password

    def generate_token(self):
        payload = {
            'username': self.username,
            'exp': datetime.utcnow() + current_app.config.get('JWT_EXPIRATION_DELTA')
        }
        self.token = jwt.encode(payload, current_app.config.get('JWT_SECRET_KEY'), algorithm='HS256')
        db.session.commit()

    @staticmethod
    def verify_token(token):
        try:
            data = jwt.decode(token, current_app.config.get('JWT_SECRET_KEY'), algorithms=["HS256"])
            username = data['username']
            user = User.query.filter_by(username=username).first()
            return user
        except jwt.ExpiredSignatureError:
            return None
        except jwt.InvalidTokenError:
            return None
