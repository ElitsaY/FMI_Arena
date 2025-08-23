import os
from dotenv import load_dotenv
import psycopg2

# Load environment variables
load_dotenv(os.path.join(os.path.dirname(__file__), "..", ".env"))

POSTGRES_USER = os.getenv("POSTGRES_USER")
POSTGRES_PW = os.getenv("POSTGRES_PW")
POSTGRES_DB = os.getenv("POSTGRES_DB")


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
