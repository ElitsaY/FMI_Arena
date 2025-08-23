import sqlite3

from models import User


class Database:
    def __init__(self, connection: sqlite3.Connection):
        self.conn = connection

    def save_user(self, user: User) -> User:
        query = (
            f"INSERT INTO users (username, email, created_at, role) VALUES (?, ?, ?, ?)"
        )
        values = (user.username, user.email, user.created_at, user.role)

        cursor = self.conn.cursor()
        cursor.execute(query, values)
        self.conn.commit()
        user.id = cursor.lastrowid
        return user

    def find_user(self, user_id: int) -> User | None:
        query = f"SELECT * FROM users WHERE id = ?"
        cursor = self.conn.cursor()
        cursor.execute(query, (user_id,))
        row = cursor.fetchone()
        if row:
            return User(
                id=row[0],
                username=row[1],
                email=row[2],
                created_at=row[3],
                role=row[4],
            )
        return None
