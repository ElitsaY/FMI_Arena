from flask import Flask
from .config import Config
from .database import db

from src.users import users_bp
from src.problems import problems_bp
from src.submissions import submissions_bp


def create_app(config_object=Config):
    app = Flask(__name__)
    app.config.from_object(config_object)

    # Initialize database
    db.init_app(app)

    app.register_blueprint(users_bp, url_prefix="/users")
    app.register_blueprint(problems_bp, url_prefix="/problems")
    app.register_blueprint(
        submissions_bp, url_prefix="/arena/<int:problem_id>/submissions"
    )

    return app
