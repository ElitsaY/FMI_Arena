import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv
import psycopg2

# Load environment variables
load_dotenv(os.path.join(os.path.dirname(__file__), "..", ".env"))

POSTGRES_USER = os.getenv("POSTGRES_USER")
POSTGRES_PW = os.getenv("POSTGRES_PW")
POSTGRES_DB = os.getenv("POSTGRES_DB")

SQLALCHEMY_DATABASE_URL = (
    f"postgresql://{POSTGRES_USER}:{POSTGRES_PW}@localhost:5432/{POSTGRES_DB}"
)

engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


# Migration execution
def run_migration():
    conn = psycopg2.connect(
        dbname=POSTGRES_DB,
        user=POSTGRES_USER,
        password=POSTGRES_PW,
        host="localhost",
        port=5432,
    )
    conn.autocommit = True

    migration_path = os.path.join(
        os.path.dirname(__file__), "resources", "db_migrations", "init.sql"
    )
    with open(migration_path, "r") as f:
        sql = f.read()
        with conn.cursor() as cur:
            cur.execute(sql)
    conn.close()


if __name__ == "__main__":
    run_migration()

DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///app.db")

engine = create_engine(DATABASE_URL, echo=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
