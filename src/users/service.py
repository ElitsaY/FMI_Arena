"""
User service module for managing user-related operations.
"""

from sqlalchemy.exc import IntegrityError
from app import db
from .models import User

session = db.session


def list_users():
    """
    Fetch all users.
    """
    return User.query.all()


def get_user(user_id):
    """
    Fetch a user by ID.
    """
    user = User.query.get(user_id)
    if not user:
        raise ValueError(f"User with id {user_id} not found")
    return user


def create_user(first_name, last_name, email):
    """
    Create a new user.
    """
    try:
        _validate_user_data(first_name, last_name, email)
    except ValueError as e:
        raise e

    user = User(first_name=first_name, last_name=last_name, email=email)
    try:
        session.add(user)
        session.commit()
        return user
    except IntegrityError as e:
        session.rollback()
        raise e


def _validate_user_data(first_name, last_name, email):
    """
    Validate user data.
    """
    if not first_name or not last_name or not email:
        raise ValueError("Missing user data")
    if User.query.filter_by(email=email).first():
        raise ValueError("Email already exists")
