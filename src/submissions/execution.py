from app import db
from .models import Submission, SubmissionStatus, SubmissionResult, SubmissionRequest
from .submission import create_submission
import time

TOTAL_TESTS = 10


def mock_submission_result(
    submission: Submission, runtime_ms: int, passed_tests: int
) -> list[SubmissionResult]:
    return [
        SubmissionResult(
            id=submission.id,
            output="Simulated output" if i < passed_tests else "Bad output",
            runtime_ms=runtime_ms,
            passed=True if i < passed_tests else False,
        )
        for i in range(TOTAL_TESTS)
    ]


def execute_submission(
    req: SubmissionRequest, runtime_ms: int, passed_tests: int
) -> list[SubmissionResult]:
    # Simulate code execution
    print("Executing submission ...")
    submission = create_submission(
        request=req,
        total_tests=TOTAL_TESTS,
        status=SubmissionStatus.RUNNING,
    )

    # Simulate execution
    time.sleep(0.1)

    submission.passed_tests = min(passed_tests, TOTAL_TESTS)
    submission.runtime_ms = runtime_ms
    submission.status = SubmissionStatus.SUCCESS
    db.session.commit()

    return mock_submission_result(submission, runtime_ms, passed_tests)
