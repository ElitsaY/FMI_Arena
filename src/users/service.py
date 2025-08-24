"""
User service module for managing user-related operations.
"""

from os import getenv
from passlib.hash import bcrypt  # type: ignore[import]
from sqlalchemy.exc import IntegrityError
from infra import db
from .models import User, Role

session = db.session

salt = getenv("PASSWORD_SALT")


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


def login_user(email: str, password: str) -> User:
    """
    Authenticate a user.
    """
    user = User.query.filter_by(email=email).first()
    if not user:
        raise ValueError("Invalid email or password")
    if not _check_password(password, user.password):
        raise ValueError("Invalid email or password")
    return user


def create_user(first_name: str, last_name: str, email: str, password: str) -> User:
    """
    Create a new user.
    """
    try:
        _validate_user_data(first_name, last_name, email, password)
    except ValueError as e:
        raise e

    hashed_password = _hash_password(password)

    user = User(
        first_name=first_name,
        last_name=last_name,
        email=email,
        password=hashed_password,
        role=Role.STUDENT,
    )
    try:
        session.add(user)
        session.commit()
        return user
    except IntegrityError as e:
        session.rollback()
        raise e


def _validate_user_data(first_name: str, last_name: str, email: str, password: str):
    """
    Validate user data.
    """
    if not first_name or not last_name or not email or not password:
        raise ValueError("Missing user data")
    if User.query.filter_by(email=email).first():
        raise ValueError("Email already exists")
    if len(password) < 6 or len(password) > 50:
        raise ValueError("Password must be between 6 and 50 characters")


def _hash_password(password: str) -> str:
    """
    Hash the user's password.
    """
    return bcrypt.hash(secret=password, salt=salt)


def _check_password(password: str, hash_password: str) -> bool:
    """
    Check the user's password.
    """
    return bcrypt.verify(secret=password.encode("utf-8"), hash=hash_password)
