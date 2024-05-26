from icecream import ic

from app.constants import MUSICIAN_TABLE
from app.db.base_queries import BaseQueries
from app.db.conn import connect_db
from app.models.musician import Musician


class MusicianQueries(BaseQueries):
    def __init__(self) -> None:
        super().__init__()
        self.table = MUSICIAN_TABLE

    def update_bio(self, musician: Musician, bio: str) -> None:
        """Updates a musician's biography in the database.

        Args:
            musician (Musician): The musician object to update
            bio (str): The new biography for the musician
        """
        db = connect_db()
        cursor = db.cursor()
        query = f"""-- sql
            UPDATE {self.table} SET bio = %s WHERE id = %s
            """
        cursor.execute(query, (bio, musician.id))
        db.commit()
        cursor.close()
        db.close()

    def update_headshot(self, musician: Musician, headshot_id: str) -> None:
        """Updates a musician's headshot ID in the database.
        The image itself is stored with Cloudinary.

        Args:
            musician (Musician): The musician object to update
            headshot_id (str): The public ID of the new headshot (as determined by Cloudinary)
        """
        db = connect_db()
        cursor = db.cursor()
        query = f"""-- sql
            UPDATE {self.table} SET headshot_id = %s WHERE id = %s
            """
        cursor.execute(query, (headshot_id, musician.id))
        db.commit()
        cursor.close()
        db.close()
