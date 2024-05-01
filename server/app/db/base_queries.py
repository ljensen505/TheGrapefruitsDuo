from typing import Callable

from app.db.conn import connect_db


class BaseQueries:
    from icecream import ic

    def __init__(self) -> None:
        self.table: str = None  # type: ignore
        self.connect_db: Callable = connect_db

    async def get_all(self) -> list[dict]:
        query = f"SELECT * FROM {self.table}"
        db = connect_db()
        cursor = db.cursor(dictionary=True)
        cursor.execute(query)
        data = cursor.fetchall()
        cursor.close()
        db.close()
        return data  # type: ignore

    async def get_one(self, id: int) -> dict | None:
        query = f"SELECT * FROM {self.table} WHERE id = %s"
        db = self.connect_db()
        cursor = db.cursor(dictionary=True)
        cursor.execute(query, (id,))
        data = cursor.fetchone()
        cursor.close()
        db.close()

        return data  # type: ignore
