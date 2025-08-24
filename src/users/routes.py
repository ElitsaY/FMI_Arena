"""
User routes for managing user-related operations.
"""

from flask import Blueprint, request, jsonify
from .service import create_user, get_user, list_users

bp = Blueprint("users", __name__, url_prefix="/users")


@bp.route("/", methods=["GET"])
def get_users():
    """
    Get a list of all users.
    """
    users = list_users()
    return jsonify([u.to_dict() for u in users])


@bp.route("/<int:user_id>", methods=["GET"])
def get_single_user(user_id):
    """
    Get a single user by ID.
    """
    try:
        user = get_user(user_id)
        return jsonify(user.to_dict())
    except ValueError as e:
        return jsonify({"error": str(e)}), 404


@bp.route("/", methods=["POST"])
def add_user():
    """
    Add a new user.
    """
    data = request.get_json()
    try:
        user = create_user(data["first_name"], data["last_name"], data["email"])
        return jsonify(user.to_dict()), 201
    except ValueError as e:
        return jsonify({"error": str(e)}), 400
