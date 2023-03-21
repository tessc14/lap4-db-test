from models import User
from flask import jsonify, request, current_app
from models import db, User
# import jwt
import datetime

# User controller

def check_authentication():
    auth_header = request.headers.get('Authorization')
    if not auth_header:
        return jsonify({'message': 'Authentication failed'}), 401
    token = auth_header.split(' ')[1]
    try:
        data = jwt.decode(token, current_app.config.get('JWT_SECRET_KEY'), algorithms=["HS256"])
        if isinstance(data, str):
            username = data
        else:
            username = data['username']
        user = User.query.filter_by(username=username).first()
        if not user:
            return jsonify({'message': 'Authentication failed'}), 401
        else:
            return jsonify({'message': 'Authentication successful'}), 200
    except jwt.ExpiredSignatureError:
        return jsonify({'message': 'Token has expired'}), 401
    except jwt.InvalidTokenError:
        return jsonify({'message': 'Invalid token'}), 401

def register_user():
    username = request.json.get('username')
    name = request.json.get('name')
    password = request.json.get('password')
    role = request.json.get('role')
    email = request.json.get('email')
    avatar = request.json.get('avatar')
    if not username or not name or not password or not role or not email:
        return jsonify({'message': 'Missing required fields'}), 400
    if User.query.filter_by(username=username).first():
        return jsonify({'message': 'Username already exists'}), 400
    user = User(username=username, name=name, password=password, role=role, email=email, avatar=avatar)
    db.session.add(user)
    db.session.commit()
    return jsonify({'message': 'User created successfully!'}), 201

def login():
    # check if user is already authenticated
    auth_header = request.headers.get('Authorization')
    if auth_header:
        token = auth_header.split(' ')[1]
        try:
            data = jwt.decode(token, current_app.config.get('JWT_SECRET_KEY'), algorithms=["HS256"])
            username = data['username']
            user = User.query.filter_by(username=username).first()
            if user:
                # update existing token with new expiration time
                expiration = datetime.utcnow() + timedelta(minutes=30)
                token = jwt.encode({'username': username, 'exp': expiration}, current_app.config.get('JWT_SECRET_KEY'), algorithm='HS256')
                return jsonify({'token': token}), 200
        except (jwt.ExpiredSignatureError, jwt.InvalidTokenError):
            pass
    # authenticate user
    username = request.json.get('username')
    password = request.json.get('password')
    user = User.query.filter_by(username=username).first()
    if not user or not user.check_password(password):
        return jsonify({'message': 'Invalid username or password'}), 401
    # generate token
    expiration = datetime.utcnow() + timedelta(minutes=30)
    token = jwt.encode({'username': username, 'exp': expiration}, current_app.config.get('JWT_SECRET_KEY'), algorithm='HS256')
    return jsonify({'token': token}), 200

def logout():
    auth_header = request.headers.get('Authorization')
    if not auth_header:
        return jsonify({'message': 'Authentication failed'}), 401
    token = auth_header.split(' ')[1]
    try:
        data = jwt.decode(token, current_app.config.get('JWT_SECRET_KEY'), algorithms=["HS256"])
        user_id = User.query.filter_by(username=data['username']).first().id
        logout_time = datetime.datetime.utcnow()
        user = User.query.filter_by(id=user_id).first()
        user.last_logout_time = logout_time
        db.session.commit()
        return jsonify({'message': 'Logout successful!'})
    except jwt.ExpiredSignatureError:
        return jsonify({'message': 'Token has expired'}), 401
    except jwt.InvalidTokenError:
        return jsonify({'message': 'Invalid token'}), 401

def create_user():
    username = request.json.get('username')
    name = request.json.get('name')
    password = request.json.get('password')
    role = request.json.get('role')
    email = request.json.get('email')
    avatar = request.json.get('avatar')
    user = User(username=username, name=name, password=password, role=role, email=email, avatar=avatar)
    db.session.add(user)
    db.session.commit()
    return jsonify({'message': 'User created successfully!'}), 201

def get_users():
    users = User.query.all()
    return jsonify(users)

def get_user(user_id):
    user = User.query.filter_by(id=user_id).first()
    if user is None:
        return jsonify({'message': 'User not found'})
    else:
        return jsonify(user)
    
def find_user_by_username(username):
    user = User.query.filter_by(username=username).first()
    if user is None:
        return jsonify({'message': 'User not found'}), 404
    else:
        return jsonify(user), 200

def update_user(user_id):
    auth_header = request.headers.get('Authorization')
    if not auth_header:
        return jsonify({'message': 'Authentication failed'}), 401
    token = auth_header.split(' ')[1]
    try:
        data = jwt.decode(token, current_app.config.get('JWT_SECRET_KEY'), algorithms=["HS256"])
        if isinstance(data, str):
            username = data
        else:
            username = data['username']
        user = User.query.filter_by(username=username).first()
        if not user:
            return jsonify({'message': 'Authentication failed'}), 401
        if user.id != user_id:
            return jsonify({'message': 'You are not authorized to update this user'}), 401
        username = request.json.get('username')
        name = request.json.get('name')
        password = request.json.get('password')
        role = request.json.get('role')
        email = request.json.get('email')
        avatar = request.json.get('avatar')
        user.username = username
        user.name = name
        user.password = password
        user.role = role
        user.email = email
        user.avatar = avatar
        db.session.commit()
        return jsonify({'message': 'User updated successfully!'})
    except jwt.ExpiredSignatureError:
        return jsonify({'message': 'Token has expired'}), 401
    except jwt.InvalidTokenError:
        return jsonify({'message': 'Invalid token'}), 401

def delete_user(user_id):
    auth_header = request.headers.get('Authorization')
    if not auth_header:
        return jsonify({'message': 'Authentication failed'}), 401
    token = auth_header.split(' ')[1]
    try:
        data = jwt.decode(token, current_app.config.get('JWT_SECRET_KEY'), algorithms=["HS256"])
        username = data['username']
        user = User.query.filter_by(username=username).first()
        if not user:
            return jsonify({'message': 'Authentication failed'}), 401
        if user.id != user_id:
            return jsonify({'message': 'You are not authorized to delete this user'}), 401
        user = User.query.filter_by(id=user_id).first()
        if user is None:
            return jsonify({'message': 'User not found'})
        else:
            db.session.delete(user)
            db.session.commit()
            return jsonify({'message': 'User deleted successfully!'})
    except jwt.ExpiredSignatureError:
        return jsonify({'message': 'Token has expired'}), 401
    except jwt.InvalidTokenError:
        return jsonify({'message': 'Invalid token'}), 401

