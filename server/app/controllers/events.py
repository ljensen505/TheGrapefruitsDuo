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

    def __init__(self, event_queries=event_queries) -> None:
        super().__init__()
        self.db: EventQueries = event_queries

    def _all_series(self, data: list[dict]) -> dict[str, EventSeries]:
        """Creates and returns a dictionary of EventSeries objects from a list of sql rows (as dicts).
        Should only be used internally.

        Args:
            data (list[dict]): List of dicts, each representing a row from the database. `event_id` may be null

        Returns:
            dict[str, EventSeries]: A dictionary of EventSeries objects, keyed by series name
        """
        all_series: dict[str, EventSeries] = {}

        for event_series_row in data:
            series_name: str = event_series_row["name"]
            if series_name not in all_series:
                all_series[series_name] = EventSeries(**event_series_row, events=[])
            if event_series_row.get("event_id"):
                all_series[series_name].events.append(Event(**event_series_row))

        return all_series

    def get_all_series(self) -> list[EventSeries]:
        """Retrieves all EventSeries objects from the database and returns them as a list.

        Raises:
            HTTPException: If any error occurs during the retrieval process (status code 500)

        Returns:
            list[EventSeries]: A list of EventSeries objects which are suitable for a response body
        """
        series_data = self.db.select_all_series()

        try:
            return [series for series in self._all_series(series_data).values()]
        except Exception as e:
            self.log_error(e)
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Error retrieving event objects: {e}",
            )

    def get_one_series_by_id(self, series_id: int) -> EventSeries:
        """Builds and returns a single EventSeries object by its numeric ID.

        Args:
            series_id (int): The numeric id of the series to retrieve

        Raises:
            HTTPException: If the series is not found (status code 404)
            HTTPException:  If an error occurs (status code 500)

        Returns:
            EventSeries: A single EventSeries object
        """
        if not (rows := self.db.select_one_by_id(series_id)):
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Event not found"
            )
        try:
            return EventSeries(
                **rows[0], events=[Event(**row) for row in rows if row.get("event_id")]
            )
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Error creating event object: {e}",
            )

    def create_series(self, series: NewEventSeries) -> EventSeries:
        """Takes a NewEventSeries object and passes it to the database layer for insertion.

        Args:
            series (NewEventSeries): A NewEventSeries object which does not yet have an ID

        Raises:
            HTTPException: If the series name already exists (status code 400)

        Returns:
            EventSeries: The newly created EventSeries object with an ID
        """
        try:
            inserted_id = self.db.insert_one_series(series)
            for new_event in series.events:
                self.db.insert_one_event(new_event, inserted_id)
            return self.get_one_series_by_id(inserted_id)
        except IntegrityError as e:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Series name already exists. Each series must have a unique name.\n{e}",
            )

    def add_series_poster(self, series_id: int, poster: UploadFile) -> EventSeries:
        """Adds (or updates) a poster image to a series.

        Args:
            series_id (int): The numeric ID of the series to update
            poster (UploadFile): The image file to upload

        Returns:
            EventSeries: The updated EventSeries object
        """
        series = self.get_one_series_by_id(series_id)
        series.poster_id = self._upload_poster(poster)
        self.db.update_series_poster(series)
        return self.get_one_series_by_id(series.series_id)

    def _upload_poster(self, poster: UploadFile) -> str:
        """Uploads a poster image to Cloudinary and returns the public ID for storage in the database.
        Should only be used internally.

        Args:
            poster (UploadFile): The image file to upload

        Raises:
            HTTPException: If an error occurs during the upload process (status code 500)

        Returns:
            str: The public ID of the uploaded image
        """
        image_file = self.verify_image(poster)
        try:
            data = uploader.upload(image_file)
            return data.get("public_id")
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Error uploading image: {e}",
            )

    def delete_series(self, id: int) -> None:
        """Ensures an EventSeries object exists and then deletes it from the database.

        Args:
            id (int): The numeric ID of the series to delete
        """
        series = self.get_one_series_by_id(id)
        self.db.delete_one_series(series)

    def update_series(self, route_id: int, series: EventSeries) -> EventSeries:
        """Updates an existing EventSeries object in the database.

        Args:
            route_id (int): The numeric ID of the series in the URL
            series (EventSeries): The updated EventSeries object

        Raises:
            HTTPException: if the ID in the URL does not match the ID in the request body (status code 400)
            HTTPException: if the poster ID is updated directly (status code 400)

        Returns:
            EventSeries: The updated EventSeries object with updated info
        """
        if route_id != series.series_id:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="ID in URL does not match ID in request body",
            )
        prev_series = self.get_one_series_by_id(series.series_id)
        if series.poster_id != prev_series.poster_id:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Poster ID cannot be updated directly. Use the /poster endpoint instead.",
            )
        self.db.delete_events_by_series(series)
        self.db.replace_series(series)
        for event in series.events:
            self.db.insert_one_event(event, series.series_id)
        return self.get_one_series_by_id(series.series_id)
