from app.constants import USER_TABLE
from app.db.base_queries import BaseQueries


class UserQueries(BaseQueries):
    def __init__(self) -> None:
        super().__init__()
        self.table = USER_TABLE

    def get_one_by_email(self, email: str) -> dict | None:
        query = f"SELECT * FROM {self.table} WHERE email = %s"
        db = self.connect_db()
        cursor = db.cursor(dictionary=True)
        cursor.execute(query, (email,))
        data = cursor.fetchone()
        cursor.close()
        db.close()

        return data

    def get_one_by_sub(self, sub: str) -> dict | None:
        query = f"SELECT * FROM {self.table} WHERE sub = %s"
        db = self.connect_db()
        cursor = db.cursor(dictionary=True)
        cursor.execute(query, (sub,))
        data = cursor.fetchone()
        cursor.close()
        db.close()

        if not data:
            return None

        return data

    def update_sub(self, email: str, sub: str) -> None:
        query = f"UPDATE {self.table} SET sub = %s WHERE email = %s"
        db = self.connect_db()
        cursor = db.cursor()
        cursor.execute(query, (sub, email))
        db.commit()
        cursor.close()
        db.close()
