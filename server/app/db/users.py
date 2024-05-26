from app.constants import USER_TABLE
from app.db.base_queries import BaseQueries


class UserQueries(BaseQueries):
    """
    Used for quering the database for User related data
    """

    def __init__(self) -> None:
        super().__init__()
        self.table = USER_TABLE

    def select_one_by_email(self, email: str) -> dict | None:
        """
        Select one user by their email address

        :param str email: user email
        :return dict | None: a dictionary of found data, or None if no user found
        """
        query = f"""-- sql
            SELECT * FROM {USER_TABLE} WHERE email = %s
            """
        cursor, conn = self.get_cursor_and_conn()
        cursor.execute(query, (email,))
        data: dict = cursor.fetchone()  # type: ignore
        self.close_cursor_and_conn(cursor, conn)

        return data

    def select_one_by_sub(self, sub: str) -> dict | None:
        """
        Select one user by their unique sub identifier

        :param str sub: user sub
        :return dict | None: a dict of user data
        """
        query = f"""-- sql
            SELECT * FROM {USER_TABLE} WHERE sub = %s
            """
        cursor, conn = self.get_cursor_and_conn()
        cursor.execute(query, (sub,))
        data: dict = cursor.fetchone()  # type: ignore
        self.close_cursor_and_conn(cursor, conn)

        return data

    def update_sub(self, email: str, sub: str) -> None:
        """
        Update user sub. Used when a user logs in for the first time.

        :param str email: user email
        :param str sub: the new unique sub identifier
        """
        query = f"""-- sql
            UPDATE {USER_TABLE} SET sub = %s WHERE email = %s
            """
        cursor, conn = self.get_cursor_and_conn()
        cursor.execute(query, (sub, email))
        conn.commit()
        self.close_cursor_and_conn(cursor, conn)
