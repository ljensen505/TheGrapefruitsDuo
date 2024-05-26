from typing import Callable

from icecream import ic
from mysql.connector.connection import MySQLConnection
from mysql.connector.cursor import MySQLCursor

from app.db.conn import connect_db


class BaseQueries:
    """
    Base class for all query classes.
    This class provides a connection to the database.

    Should not be used directly; instead, inherit from this class and provide the table name.
    """

    def __init__(self) -> None:
        self.table: str = None  # type: ignore
        self.connect_db: Callable[[], MySQLConnection] = connect_db

    def select_all(self) -> list[dict]:
        query = f"""-- sql
            SELECT * FROM {self.table}
            """
        cursor, conn = self.get_cursor_and_conn()
        cursor.execute(query)
        data: list[dict] = cursor.fetchall()  # type: ignore
        self.close_cursor_and_conn(cursor, conn)

        fake_query = f"""-- sql
            select * from dogs
        """

        return data

    def select_one_by_id(self, id: int) -> dict | None:
        query = f"""-- sql
            SELECT * FROM {self.table} WHERE id = %s
            """
        cursor, conn = self.get_cursor_and_conn()
        cursor.execute(query, (id,))
        data: dict | None = cursor.fetchone()  # type: ignore
        self.close_cursor_and_conn(cursor, conn)

        return data

    def get_cursor_and_conn(self) -> tuple[MySQLCursor, MySQLConnection]:
        conn = self.connect_db()
        cursor = conn.cursor(dictionary=True)
        return cursor, conn

    def close_cursor_and_conn(self, cursor: MySQLCursor, conn: MySQLConnection) -> None:
        cursor.close()
        conn.close()
