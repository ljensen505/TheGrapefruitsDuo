from asyncio import gather

from icecream import ic

from app.db.base_queries import BaseQueries
from app.models.event import (
    EVENT_TABLE,
    SERIES_TABLE,
    Event,
    EventSeries,
    NewEvent,
    NewEventSeries,
)


class EventQueries(BaseQueries):
    def __init__(self) -> None:
        super().__init__()
        self.table = SERIES_TABLE

    async def get_one(self, series_id: int) -> list[dict] | None:
        query = f"""
            SELECT *
            FROM {SERIES_TABLE}
            INNER JOIN {EVENT_TABLE}
            ON {SERIES_TABLE}.series_id = {EVENT_TABLE}.series_id
            WHERE {SERIES_TABLE}.series_id = %s
        """

        db = self.connect_db()
        cursor = db.cursor(dictionary=True)
        cursor.execute(query, (series_id,))
        data = cursor.fetchall()
        cursor.close()
        db.close()
        return data

    async def get_all(self) -> list[dict]:
        query = f"""
                SELECT * 
                FROM {SERIES_TABLE}
                INNER JOIN {EVENT_TABLE}
                ON {SERIES_TABLE}.series_id = {EVENT_TABLE}.series_id
            """

        db = self.connect_db()
        cursor = db.cursor(dictionary=True)
        cursor.execute(query)
        data = cursor.fetchall()
        cursor.close()
        db.close()
        return data

    async def insert_one_series(self, series: NewEventSeries) -> int:
        query = f"INSERT INTO {self.table} (name, description) VALUES (%s, %s)"
        db = self.connect_db()
        cursor = db.cursor()
        cursor.execute(
            query,
            (
                series.name,
                series.description,
            ),
        )
        inserted_id = cursor.lastrowid
        db.commit()
        cursor.close()
        db.close()
        return inserted_id

    async def insert_one_event(self, event: NewEvent, series_id: int) -> int:
        query = f"INSERT INTO {EVENT_TABLE} (series_id, location, time, ticket_url, map_url) VALUES (%s, %s, %s, %s, %s)"
        db = self.connect_db()
        cursor = db.cursor()
        ticket_url = str(event.ticket_url) if event.ticket_url else None
        map_url = str(event.map_url) if event.map_url else None
        cursor.execute(
            query, (series_id, event.location, event.time, ticket_url, map_url)
        )
        iserted_id = cursor.lastrowid
        db.commit()
        cursor.close()
        db.close()
        return iserted_id

    async def delete_events_by_series(self, series: EventSeries) -> None:
        query = f"DELETE FROM {EVENT_TABLE} WHERE series_id = %s"
        db = self.connect_db()
        cursor = db.cursor()
        cursor.execute(query, (series.series_id,))
        db.commit()
        cursor.close()

    async def delete_one_series(self, series: EventSeries) -> None:
        query = f"DELETE FROM {self.table} WHERE series_id = %s"
        db = self.connect_db()
        cursor = db.cursor()
        cursor.execute(query, (series.series_id,))
        db.commit()
        cursor.close()

    async def update_series_poster(self, series: EventSeries) -> None:
        query = f"UPDATE {self.table} SET poster_id = %s WHERE series_id = %s"
        db = self.connect_db()
        cursor = db.cursor()
        cursor.execute(query, (series.poster_id, series.series_id))
        db.commit()
        cursor.close()

    async def replace_event(self, event: Event) -> None:
        query = f"""
        UPDATE {EVENT_TABLE}
        SET location = %s, time = %s, ticket_url = %s, map_url = %s
        WHERE event_id = %s
        """
        db = self.connect_db()
        cursor = db.cursor()
        ticket_url = str(event.ticket_url) if event.ticket_url else None
        map_url = str(event.map_url) if event.map_url else None
        cursor.execute(
            query, (event.location, event.time, ticket_url, map_url, event.event_id)
        )
        db.commit()
        cursor.close()
        db.close()

    async def replace_series(self, series: EventSeries) -> None:
        query = f"""
        UPDATE {self.table}
        SET name = %s, description = %s, poster_id = %s
        WHERE series_id = %s
        """
        db = self.connect_db()
        cursor = db.cursor()
        cursor.execute(
            query, (series.name, series.description, series.poster_id, series.series_id)
        )
        db.commit()
        cursor.close()
        db.close()
