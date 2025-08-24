"""
Submissions routes for managing user submissions to problems.
"""

from flask import Blueprint, request, jsonify
from .submission import get_submissions_by_problem
from .execution import execute_submission
from .models import Submission, SubmissionResult, SubmissionRequest


bp = Blueprint(
    "submissions", __name__, url_prefix="/arena/<int:problem_id>/submissions"
)


@bp.route("/", methods=["GET"])
def fetch_submissions(problem_id: int) -> list[Submission]:
    """Fetch submissions for a specific problem."""
    print("Fetching submissions for problem:", problem_id)
    created_by = request.args.get("created_by", type=int, default=None)
    submissions = get_submissions_by_problem(
        problem_id=problem_id, created_by=created_by
    )
    print(f"Found {len(submissions)} submissions")
    print(type(submissions[0]) if submissions else None)
    return jsonify([s.to_dict() for s in submissions if s is not None]), 200


@bp.route("/", methods=["POST"])
def execute_submission_route(problem_id: int) -> list[SubmissionResult]:
    """Execute a user submission for a specific problem."""
    data = request.json
    submission = SubmissionRequest(
        user_id=data.get("user_id"),
        problem_id=problem_id,
        source_code=data.get("source_code"),
        language=data.get("language"),
    )

    try:
        # Execute the submission and return the results
        results = execute_submission(
            submission, data.get("runtime_ms", 1000), data.get("passed_tests", 7)
        )
        return jsonify(results), 200
    except ValueError as e:
        return jsonify({"error": str(e)}), 400
