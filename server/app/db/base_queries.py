from typing import Callable

from icecream import ic

from app.db.conn import connect_db


class BaseQueries:
    """
    Base class for all query classes.
    This class provides a connection to the database.

    Should not be used directly; instead, inherit from this class and provide the table name.
    """

    def __init__(self) -> None:
        self.table: str = None  # type: ignore
        self.connect_db: Callable = connect_db

    def select_all_series(self) -> list[dict]:
        query = f"SELECT * FROM {self.table}"
        db = connect_db()
        cursor = db.cursor(dictionary=True)
        cursor.execute(query)
        data = cursor.fetchall()
        cursor.close()
        db.close()
        return data  # type: ignore

    def select_one_by_id(self, id: int) -> dict | None:
        query = f"SELECT * FROM {self.table} WHERE id = %s"
        db = self.connect_db()
        cursor = db.cursor(dictionary=True)
        cursor.execute(query, (id,))
        data = cursor.fetchone()
        cursor.close()
        db.close()

        return data  # type: ignore
