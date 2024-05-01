from icecream import ic

from app.db.base_queries import BaseQueries
from app.db.conn import connect_db
from app.models.musician import MUSICIAN_TABLE


class MusicianQueries(BaseQueries):
    def __init__(self) -> None:
        super().__init__()
        self.table = MUSICIAN_TABLE

    async def update_bio(self, id: int, bio: str) -> None:
        db = connect_db()
        cursor = db.cursor()
        query = f"UPDATE {self.table} SET bio = %s WHERE id = %s"
        cursor.execute(query, (bio, id))
        db.commit()
        cursor.close()
        db.close()

    async def update_headshot(self, id: int, headshot_id: str) -> None:
        db = connect_db()
        cursor = db.cursor()
        query = f"UPDATE {self.table} SET headshot_id = %s WHERE id = %s"
        cursor.execute(query, (headshot_id, id))
        db.commit()
        cursor.close()
        db.close()
