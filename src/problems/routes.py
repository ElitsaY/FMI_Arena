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
    try:
        problem = problem_service.get_problem(problem_id)
        return jsonify(problem.to_dict())
    except ValueError as e:
        return jsonify({"error": str(e)}), 404


@bp.route("/", methods=["POST"])
def create_problem():
    data = request.json
    try:
        problem = problem_service.create_problem(**data)
        return jsonify(problem.to_dict()), 201
    except ValueError as e:
        return jsonify({"error": str(e)}), 400


@bp.route("/<int:problem_id>/tags", methods=["PUT"])
def assign_tag(problem_id):
    data = request.json
    tag = data.get("tag")
    if not tag:
        return jsonify({"error": "Tag is required"}), 400
    problem = problem_service.assign_tag(problem_id, tag)
    return jsonify(problem.to_dict())
