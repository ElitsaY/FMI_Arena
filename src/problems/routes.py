"""
Routes for managing problems-submission related operations.
"""

from flask import Blueprint, request, jsonify
from flask.wrappers import Response
from .models import CreateProblemRequest
from .service import ProblemService

bp = Blueprint("problems", __name__)
problem_service = ProblemService()  # shared service instance


@bp.route("/", methods=["GET"])
def list_problems() -> tuple[Response, int]:
    """
    List all problems.
    """
    tags_list = request.args.getlist("tags")
    problems = problem_service.list_problems(tags=tags_list if tags_list else None)
    return jsonify([p.to_dict() for p in problems]), 200


@bp.route("/<int:problem_id>", methods=["GET"])
def get_problem(problem_id: int) -> tuple[Response, int]:
    """
    Get a single problem by ID.
    """
    try:
        problem = problem_service.get_problem(problem_id)
        return jsonify(problem.to_dict()), 200
    except ValueError as e:
        return jsonify({"error": str(e)}), 404


@bp.route("/", methods=["POST"])
def create_problem() -> tuple[Response, int]:
    """
    Submit a new problem.
    """
    data = request.json
    if not data:
        return jsonify({"error": "Missing body"}), 400

    try:
        problem = problem_service.create_problem(
            CreateProblemRequest(**data), data["created_by"]
        )
        return jsonify(problem.to_dict()), 201
    except ValueError as e:
        return jsonify({"error": str(e)}), 400


@bp.route("/<int:problem_id>/tags", methods=["PUT"])
def assign_tag(problem_id: int) -> tuple[Response, int]:
    """
    Assign a tag to a problem.
    """
    data = request.json
    if not data:
        return jsonify({"error": "Missing body"}), 400

    tag = data.get("tag")
    if not tag:
        return jsonify({"error": "Tag is required"}), 400
    problem = problem_service.assign_tag(problem_id, tag)
    return jsonify(problem.to_dict()), 200
