from app import db
from .models import User
from sqlalchemy.exc import IntegrityError

session = db.session


def list_users():
    return User.query.all()


def get_user(user_id):
    user = User.query.get(user_id)
    if not user:
        raise ValueError(f"User with id {user_id} not found")
    return user


def create_user(first_name, last_name, email):
    user = User(first_name=first_name, last_name=last_name, email=email)
    try:
        session.add(user)
        session.commit()
        return user
    except IntegrityError:
        session.rollback()
        raise ValueError("Email already exists")


def validate_user_data(first_name, last_name, email):
    if not first_name or not last_name or not email:
        raise ValueError("Missing user data")
    if User.query.filter_by(email=email).first():
        raise ValueError("Email already exists")
    return None
