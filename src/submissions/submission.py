"""
Handling problem submission
"""

import hashlib
from sqlalchemy.exc import IntegrityError
from sqlalchemy import desc, case

from infra import db
from .models import Submission, SubmissionStatus, SubmissionRequest


def md5_hash(code: str) -> str:
    """
    Generate MD5 hash for the given code.
    """
    return hashlib.md5(code.encode("utf-8")).hexdigest()


def create_submission(
    request: SubmissionRequest,
    total_tests: int,
    status: SubmissionStatus = SubmissionStatus.DRAFT,
) -> Submission:
    """
    Create a new submission from request.
    """
    code_md5 = md5_hash(request.source_code)

    existing = Submission.query.filter_by(
        user_id=request.user_id, problem_id=request.problem_id, code_md5=code_md5
    ).first()
    if existing:
        raise ValueError("Duplicate submission")

    submission = Submission(
        user_id=request.user_id,
        problem_id=request.problem_id,
        code=request.source_code,
        code_md5=code_md5,
        language=request.language,
        status=status,
        passed_tests=0,
        total_tests=total_tests,
        runtime_ms=None,
    )
    db.session.add(submission)
    try:
        db.session.commit()
    except IntegrityError:
        db.session.rollback()
        raise
    return submission


def get_submissions_by_problem(
    problem_id: int,
    created_by: int | None = None,
) -> list[Submission]:
    """
    List submissions by problem ID and optional creator ID.
    """
    score = case(
        (
            Submission.total_tests > 0,
            Submission.passed_tests / Submission.total_tests,
        ),
        else_=0,
    ).label("score")

    query = db.session.query(Submission)
    if created_by is not None:
        query = query.filter_by(problem_id=problem_id, created_by=created_by)
    else:
        query = query.filter_by(problem_id=problem_id)
    # Ensure the results are Submission objects and ordered by score descending
    submissions = query.order_by(desc(score)).all()
    return submissions
