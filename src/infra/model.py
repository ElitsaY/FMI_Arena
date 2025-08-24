"""
Defines a base model for the application.
"""

from .database import db


class Base(db.Model):  # type: ignore # pylint: disable=R0903
    """Base model for all database models."""

    __abstract__ = True
