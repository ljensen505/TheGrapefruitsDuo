from app.db.base_queries import BaseQueries
from app.models.group import GROUP_TABLE


class GroupQueries(BaseQueries):
    def __init__(self) -> None:
        super().__init__()
        self.table = GROUP_TABLE

    async def get_one(self) -> dict:
        query = f"SELECT * FROM {self.table}"
        db = self.connect_db()
        cursor = db.cursor(dictionary=True)
        cursor.execute(query)
        data = cursor.fetchone()
        cursor.close()
        db.close()

        if not data:
            raise Exception("error retrieving group")

        return data

    async def get_all(self) -> None:
        raise NotImplementedError(
            "get_all method not implemented for GroupQueries. There's only one row in the table."
        )

    async def update_group_bio(self, bio: str) -> None:
        db = self.connect_db()
        cursor = db.cursor()
        query = f"UPDATE {self.table} SET bio = %s WHERE id = 1"  # only one row in the table
        cursor.execute(query, (bio,))
        db.commit()
        cursor.close()
        db.close()
