from fastapi import HTTPException, UploadFile, status
from icecream import ic
from mysql.connector.errors import IntegrityError

from app.admin.images import uploader
from app.controllers.base_controller import BaseController
from app.db import event_queries
from app.db.events import EventQueries
from app.models.event import Event, EventSeries, NewEventSeries


class EventController(BaseController):
    def __init__(self) -> None:
        super().__init__()
        self.db: EventQueries = event_queries

    def _all_series(self, data: list[dict]) -> list[EventSeries]:
        all_series: dict[str, EventSeries] = {}

        for event_series_row in data:
            series_name: str = event_series_row["name"]
            if series_name not in all_series:
                all_series[series_name] = EventSeries(**event_series_row, events=[])
            if event_series_row.get("event_id"):
                all_series[series_name].events.append(Event(**event_series_row))

        return [series for series in all_series.values()]

    async def get_all_series(self) -> list[EventSeries]:
        series_data = await self.db.select_all_series()

        try:
            return self._all_series(series_data)
        except Exception as e:
            self.log_error(e)
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Error retrieving event objects: {e}",
            )

    async def get_one_series_by_id(self, series_id: int) -> EventSeries:
        if not (data := await self.db.select_one_series_by_id(series_id)):
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Event not found"
            )
        try:
            return EventSeries(
                **data[0], events=[Event(**e) for e in data if e["event_id"]]
            )
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Error creating event object: {e}",
            )

    async def create_series(self, series: NewEventSeries) -> EventSeries:
        try:
            inserted_id = await self.db.insert_one_series(series)
            for new_event in series.events:
                await self.db.insert_one_event(new_event, inserted_id)
            return await self.get_one_series_by_id(inserted_id)
        except IntegrityError as e:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Series name already exists. Each series must have a unique name.\n{e}",
            )

    async def add_series_poster(self, series_id, poster: UploadFile) -> EventSeries:
        series = await self.get_one_series_by_id(series_id)
        series.poster_id = await self._upload_poster(poster)
        await self.db.update_series_poster(series)
        return await self.get_one_series_by_id(series.series_id)

    async def _upload_poster(self, poster: UploadFile) -> str:
        image_file = await self.verify_image(poster)
        try:
            data = uploader.upload(image_file)
            return data.get("public_id")
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Error uploading image: {e}",
            )

    async def delete_series(self, id: int) -> None:
        series = await self.get_one_series_by_id(id)
        await self.db.delete_one_series(series)

    async def update_series(self, route_id: int, series: EventSeries) -> EventSeries:
        if route_id != series.series_id:
            print("error")
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="ID in URL does not match ID in request body",
            )
        prev_series = await self.get_one_series_by_id(series.series_id)
        if series.poster_id != prev_series.poster_id:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Poster ID cannot be updated directly. Use the /poster endpoint instead.",
            )
        await self.db.delete_events_by_series(series)
        await self.db.replace_series(series)
        for event in series.events:
            await self.db.insert_one_event(event, series.series_id)
        return await self.get_one_series_by_id(series.series_id)
