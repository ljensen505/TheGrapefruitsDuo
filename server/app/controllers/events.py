from fastapi import HTTPException, UploadFile, status
from icecream import ic
from mysql.connector.errors import IntegrityError

from app.admin.images import uploader
from app.controllers.base_controller import BaseController
from app.db import event_queries
from app.db.events import EventQueries
from app.models.event import Event, EventSeries, NewEventSeries


class EventController(BaseController):
    """
    Handles all event-related operations and serves as an intermediate controller between
    the main controller and the model layer.
    Inherits from BaseController, which provides logging and other generic methods.

    Testing: pass a mocked EventQueries object to the constructor.
    """

    def __init__(self, eq=event_queries) -> None:
        super().__init__()
        self.db: EventQueries = eq

    def _all_series(self, data: list[dict]) -> dict[str, EventSeries]:
        """
        Helper method to instantiate EventSeries objects from sql rows (a list of dictionaries).
        Instantiation is done by destructuring the dictionary into the EventSeries constructor.
        Should not be called directly; use get_all_series() instead.
        series.name is a required and unique field and can reliably be used as a key in a dictionary.
        """
        all_series: dict[str, EventSeries] = {}

        for event_series_row in data:
            series_name: str = event_series_row["name"]
            if series_name not in all_series:
                all_series[series_name] = EventSeries(**event_series_row, events=[])
            if event_series_row.get("event_id"):
                all_series[series_name].events.append(Event(**event_series_row))

        return all_series

    async def get_all_series(self) -> list[EventSeries]:
        """
        Attempts to create and return a list of EventSeries objects and is consumed by the main controller.
        Will trigger a 500 status code if any exception is raised, and log the error to a timestamped text file.

        The list of EventSeries is created by calling the _all_series() helper method, which provided this data
        as a list of dicts.
        """
        series_data = await self.db.select_all_series()

        try:
            return [series for series in self._all_series(series_data).values()]
        except Exception as e:
            self.log_error(e)
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Error retrieving event objects: {e}",
            )

    async def get_one_series_by_id(self, series_id: int) -> EventSeries:
        """
        Builds and returns a single EventSeries object by its numeric ID.
        """
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
        """
        Takes a NewEventSeries object and passes it to the database layer for insertion.
        """
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
        """
        Adds (or updates) a poster image to a series.
        Actual image storage is done with Cloudinary and the public ID is stored in the database.
        """
        series = await self.get_one_series_by_id(series_id)
        series.poster_id = await self._upload_poster(poster)
        await self.db.update_series_poster(series)
        return await self.get_one_series_by_id(series.series_id)

    async def _upload_poster(self, poster: UploadFile) -> str:
        """
        Uploads a poster image to Cloudinary and returns the public ID for storage in the database.
        """
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
        """
        Ensures an EventSeries object exists and then deletes it from the database
        """
        series = await self.get_one_series_by_id(id)
        await self.db.delete_one_series(series)

    async def update_series(self, route_id: int, series: EventSeries) -> EventSeries:
        """
        Updates an existing EventSeries object in the database.
        """
        if route_id != series.series_id:
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
