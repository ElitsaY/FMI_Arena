"""
Manage database connection
"""

import os
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv


load_dotenv()  # Loads variables from .env into os.environ

POSTGRES_USER = os.getenv("POSTGRES_USER")
POSTGRES_PW = os.getenv("POSTGRES_PW")
POSTGRES_DB = os.getenv("POSTGRES_DB")
POSTGRES_HOST = os.getenv("POSTGRES_HOST")

SQLALCHEMY_DATABASE_URI = (
    f"postgresql://{POSTGRES_USER}:{POSTGRES_PW}@{POSTGRES_HOST}/{POSTGRES_DB}"
)
db = SQLAlchemy()
