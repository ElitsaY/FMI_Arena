"""Submission models for managing user submissions to problems."""

from enum import Enum
from dataclasses import asdict, dataclass
from typing import Optional, Any

from app import db


class SubmissionStatus(Enum):
    """Submission statuses."""

    DRAFT = "draft"
    RUNNING = "running"
    SUCCESS = "success"
    FAILED = "failed"

    def __str__(self):
        return self.value


class Submission(db.Model):  # pylint: disable=R0903
    """Submission model for user code submissions."""

    __tablename__ = "submissions"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    problem_id = db.Column(db.Integer, db.ForeignKey("problems.id"), nullable=False)
    code = db.Column(db.Text, nullable=False)
    code_md5 = db.Column(db.String(32), nullable=False)
    language = db.Column(db.String(50), nullable=False)
    status = db.Column(db.Enum(SubmissionStatus), nullable=False)
    submitted_at = db.Column(db.DateTime, server_default=db.func.now())
    passed_tests = db.Column(db.Integer, default=0)
    total_tests = db.Column(db.Integer, default=0)
    runtime_ms = db.Column(db.Integer)
    extra_metadata = db.Column(db.JSON)

    def to_dict(self):
        """Convert the Submission instance to a dictionary."""
        return {
            "id": self.id,
            "user_id": self.user_id,
            "problem_id": self.problem_id,
            "code": self.code,
            "code_md5": self.code_md5,
            "language": self.language,
            "status": str(self.status),
            "submitted_at": self.submitted_at,
            "passed_tests": self.passed_tests,
            "total_tests": self.total_tests,
            "runtime_ms": self.runtime_ms,
            "extra_metadata": self.extra_metadata,
        }


@dataclass
class TestResult:
    """Test result for a single test case."""

    input: Any
    expected_output: Any
    actual_output: Any
    passed: bool
    runtime_ms: Optional[float] = None  # Optional, in milliseconds

    def to_dict(self):
        """Convert the TestResult instance to a dictionary."""
        return asdict(self)


@dataclass
class SubmissionResult:
    """Submission result for a single submission."""

    id: int
    output: str
    runtime_ms: int
    passed: bool


class SubmissionRequest:  # pylint: disable=R0903
    """Submission request for creating a new submission."""

    def __init__(self, user_id: int, problem_id: int, source_code: str, language: str):
        self.user_id = user_id
        self.problem_id = problem_id
        self.source_code = source_code
        self.language = language

    def to_dict(self):
        """
        Convert the SubmissionRequest instance to a dictionary.
        """
        return {
            "user_id": self.user_id,
            "problem_id": self.problem_id,
            "source_code": self.source_code,
            "language": self.language,
        }
