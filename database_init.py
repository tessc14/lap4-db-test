from app import app
from database import db
from models import User
from datetime import datetime, timedelta
from werkzeug.security import generate_password_hash

with app.app_context():

    # Drop all tables if they already exist
    db.drop_all()
    # Create the tables
    db.create_all()

    # Add some users
    user1 = User(
        username="user1",
        name="User One",
        password="password1",
        role="leader",
        email="user1@example.com",
        avatar="avatar1.png",
    )
    db.session.add(user1)

    user2 = User(
        username="user2",
        name="User Two",
        password="password2",
        role="member",
        email="user2@example.com",
        avatar="avatar2.png",
    )
    db.session.add(user2)


    # Commit the users
    db.session.commit()
 