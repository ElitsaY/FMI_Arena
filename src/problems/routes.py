from flask import Blueprint, request, jsonify
from .service import ProblemService

bp = Blueprint("problems", __name__)
problem_service = ProblemService()  # shared service instance


@bp.route("/", methods=["GET"])
def list_problems():
    tags = request.args.get("tags")
    problems = problem_service.list_problems(tags=tags.split(",") if tags else None)
    return jsonify([p.to_dict() for p in problems])


@bp.route("/<int:problem_id>", methods=["GET"])
def get_problem(problem_id):
    problem = problem_service.get_problem(problem_id)
    return jsonify(problem.to_dict())


@bp.route("/", methods=["POST"])
def create_problem():
    data = request.json
    problem = problem_service.create_problem(
        name=data["name"],
        description=data["description"],
        input_format=data["input_format"],
        output_format=data["output_format"],
        extra_metadata=data.get("extra_metadata", {}),
        test_cases=data["test_cases"],
        created_by=data["created_by"],
    )
    return jsonify(problem.to_dict()), 201


@bp.route("/<int:problem_id>/tags", methods=["PUT"])
def assign_tag(problem_id):
    data = request.json
    tag = data.get("tag")
    if not tag:
        return jsonify({"error": "Tag is required"}), 400
    problem = problem_service.assign_tag(problem_id, tag)
    return jsonify(problem.to_dict())
