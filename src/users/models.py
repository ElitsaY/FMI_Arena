"""
User model for representing users in the system.
"""

from enum import Enum
from infra import db


class Role(Enum):
    """
    User roles in the system.
    """

    GUEST = "guest"
    STUDENT = "student"
    ADMIN = "admin"

    def __str__(self):
        """
        String representation of the role.
        """
        return self.value


class User(db.Model):  # pylint: disable=R0903
    """
    User model for representing users in the system.
    """

    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(80), nullable=False)
    last_name = db.Column(db.String(80), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(128), nullable=False, default="hashed_password")
    role = db.Column(db.Enum(Role), default=Role.GUEST)

    def to_dict(self):
        """
        Convert the user model to a dictionary.
        """
        return {
            "id": self.id,
            "first_name": self.first_name,
            "last_name": self.last_name,
            "email": self.email,
            "password": self.password,
            "role": str(self.role),
        }
