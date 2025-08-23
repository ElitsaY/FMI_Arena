from app import db
from .models import User
from sqlalchemy.exc import IntegrityError


class UserService:
    def __init__(self, session=None):
        self.session = session or db.session

    def list_users(self):
        return User.query.all()

    def get_user(self, user_id):
        user = User.query.get(user_id)
        if not user:
            raise ValueError(f"User with id {user_id} not found")
        return user

    def create_user(self, first_name, last_name, email):
        user = User(first_name=first_name, last_name=last_name, email=email)
        try:
            self.session.add(user)
            self.session.commit()
            return user
        except IntegrityError:
            self.session.rollback()
            raise ValueError("Email already exists")

    def validate_user_data(self, first_name, last_name, email):
        if not first_name or not last_name or not email:
            raise ValueError("Missing user data")
        if User.query.filter_by(email=email).first():
            raise ValueError("Email already exists")
        return None
