from flask import Blueprint, request, jsonify
from .service import UserService

bp = Blueprint("users", __name__)
user_service = UserService()  # shared service instance


@bp.route("/", methods=["GET"])
def get_users():
    users = user_service.list_users()
    return jsonify([u.to_dict() for u in users])


@bp.route("/<int:user_id>", methods=["GET"])
def get_single_user(user_id):
    try:
        user = user_service.get_user(user_id)
        return jsonify(user.to_dict())
    except ValueError as e:
        return jsonify({"error": str(e)}), 404


@bp.route("/", methods=["POST"])
def add_user():
    data = request.get_json()
    try:
        user_service.validate_user_data(
            data.get("first_name"), data.get("last_name"), data.get("email")
        )
    except ValueError as e:
        return jsonify({"error": str(e)}), 400

    try:
        user = user_service.create_user(
            data["first_name"], data["last_name"], data["email"]
        )
        return jsonify(user.to_dict()), 201
    except ValueError as e:
        return jsonify({"error": str(e)}), 400
