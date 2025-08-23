from os import getenv


class Config:
    dbname = getenv("POSTGRES_DB")
    user = getenv("POSTGRES_USER")
    password = getenv("POSTGRES_PW")
    host = getenv("POSTGRES_HOST")
    port = getenv("POSTGRES_PORT", 5432)
    SQLALCHEMY_DATABASE_URI = f"postgresql://{user}:{password}@{host}:{port}/{dbname}"
    SQLALCHEMY_TRACK_MODIFICATIONS = False  # performance
