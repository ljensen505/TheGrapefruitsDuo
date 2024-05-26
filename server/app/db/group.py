from app.constants import GROUP_TABLE
from app.db.base_queries import BaseQueries


class GroupQueries(BaseQueries):
    def __init__(self) -> None:
        super().__init__()
        self.table = GROUP_TABLE

    def select_one_by_id(self) -> dict:
        query = f"""-- sql
            SELECT * FROM {self.table}
            """
        cursor, conn = self.get_cursor_and_conn()
        cursor.execute(query)
        data: dict = cursor.fetchone()  # type: ignore
        self.close_cursor_and_conn(cursor, conn)

        if not data:
            raise Exception("error retrieving group")

        return data

    def select_all(self) -> None:
        raise NotImplementedError(
            "get_all method not implemented for GroupQueries. There's only one row in the table."
        )

    def update_group_bio(self, bio: str) -> None:
        cursor, conn = self.get_cursor_and_conn()
        query = f"""-- sql
            UPDATE {self.table} SET bio = %s WHERE id = 1
            """  # only one row in the table
        cursor.execute(query, (bio,))
        conn.commit()
        self.close_cursor_and_conn(cursor, conn)
