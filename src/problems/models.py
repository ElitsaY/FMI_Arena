"""
This module defines the Problem SQLAlchemy model.
The TestCase dataclass for representing programming problems and their test cases.
"""

from dataclasses import dataclass, asdict
from infra import db, Base


class Problem(Base):  # pylint: disable=R0903
    """
    SQLAlchemy model for storing problem details,
      formats, metadata, test cases, and creator information.
    """

    __tablename__ = "problems"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    description = db.Column(db.Text, nullable=False)
    input_format = db.Column(db.Text, nullable=True)
    output_format = db.Column(db.Text, nullable=False)
    extra_metadata = db.Column(db.JSON, nullable=True)
    test_cases = db.Column(db.JSON, nullable=False)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    created_by = db.Column(db.Integer, foreign_key="users.id", nullable=False)

    def to_dict(self):
        """Convert the Problem instance to a dictionary."""
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "input_format": self.input_format,
            "output_format": self.output_format,
            "extra_metadata": self.extra_metadata,
            "test_cases": self.test_cases,
            "created_at": self.created_at,
            "created_by": self.created_by,
        }


@dataclass
class TestCase:
    """Dataclass for representing individual test cases with input and output data."""

    input: dict
    output: dict

    def to_dict(self):
        """Convert the TestCase instance to a dictionary."""
        return asdict(self)


@dataclass
class CreateProblemRequest:
    """Dataclass for representing a request to create a new problem."""

    name: str
    description: str
    input_format: str
    output_format: str
    extra_metadata: dict
    test_cases: list[TestCase]

    def to_dict(self):
        """Convert the CreateProblemRequest instance to a dictionary."""
        return asdict(self)
