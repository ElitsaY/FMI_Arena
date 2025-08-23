from app import db
from dataclasses import dataclass, asdict


class Problem(db.Model):
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
    input: dict
    output: dict

    def to_dict(self):
        return asdict(self)
