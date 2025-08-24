from enum import Enum
from app import db
from dataclasses import asdict, dataclass
from typing import Optional, Any


class SubmissionStatus(Enum):
    DRAFT = "draft"
    RUNNING = "running"
    SUCCESS = "success"
    FAILED = "failed"

    def __str__(self):
        return self.value


class Submission(db.Model):
    __tablename__ = "submissions"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    problem_id = db.Column(db.Integer, db.ForeignKey(
        "problems.id"), nullable=False)
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
    input: Any
    expected_output: Any
    actual_output: Any
    passed: bool
    runtime_ms: Optional[float] = None  # Optional, in milliseconds

    def to_dict(self):
        return asdict(self)


@dataclass
class SubmissionResult:
    id: int
    output: str
    runtime_ms: int
    passed: bool


class SubmissionRequest:
    def __init__(self, user_id: int, problem_id: int, source_code: str, language: str):
        self.user_id = user_id
        self.problem_id = problem_id
        self.source_code = source_code
        self.language = language

    def to_dict(self):
        return {
            "user_id": self.user_id,
            "problem_id": self.problem_id,
            "source_code": self.source_code,
            "language": self.language,
        }
