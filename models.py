from database import db

class User(db.Model):
    __tablename__ = "users"
    id = db.Column(db.String(32), primary_key=True, unique=True)
    username = db.Column(db.String(35), unique=True)
    password = db.Column(db.Text, nullable=False)
