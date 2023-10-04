from App.models import User
from App.database import db

def create_user(username, password, email):
    newuser = User(username=username, password=password, email=email, rank=0, is_admin=False, results = 0)
    try:
        db.session.add(newuser)
        db.session.commit()
        return newuser
    except:
        return None

def create_admin(username, password, email):
    newadmin = User(username=username, password=password, email=email, rank=0, is_admin=True, results=0)
    try:
        db.session.add(newadmin)
        db.session.commit()
        return newadmin
    except:
        return None

def get_user_by_username(username):
    return User.query.filter_by(username=username).first()

def get_user(id):
    return User.query.get(id)

def get_all_users():
    return User.query.all()

def get_all_users_json():
    users = User.query.all()
    if not users:
        return []
    users = [user.get_json() for user in users]
    return users

def update_user(id, username):
    user = get_user(id)
    if user:
        user.username = username
        db.session.add(user)
        return db.session.commit()
    return None
    