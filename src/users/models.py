from enum import Enum
from app import db


class Role(Enum):
    GUEST = "guest"
    STUDENT = "student"
    ADMIN = "admin"

    def __str__(self):
        return self.value


class User(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(80), nullable=False)
    last_name = db.Column(db.String(80), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(128), nullable=False,
                         default="hashed_password")
    role = db.Column(db.Enum(Role), default=Role.GUEST)

    def to_dict(self):
        return {
            "id": self.id,
            "first_name": self.first_name,
            "last_name": self.last_name,
            "email": self.email,
            "password": self.password,
            "role": str(self.role),
        }
