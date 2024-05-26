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
    Handles all event-related operations.
    Inherits from BaseController, which provides logging and other generic methods.
    """

    def __init__(self, event_queries: EventQueries = event_queries) -> None:
        """
        Initializes the EventController with an EventQueries object.

        :param EventQueries event_queries: object for querying event data, defaults to event_queries
        """
        super().__init__()
        self.db: EventQueries = event_queries

    def _all_series(self, data_rows: list[dict]) -> dict[str, EventSeries]:
        """
        Builds a dictionary of EventSeries objects from a list of dictionaries.
        Must only be used internally.

        :param list[dict] data_rows: The list of sql rows as dictionaries
        :return dict[str, EventSeries]: A dictionary of EventSeries objects keyed by series name
        """
        all_series: dict[str, EventSeries] = {}

        for event_series_row in data_rows:
            series_name: str = event_series_row["name"]
            if series_name not in all_series:
                all_series[series_name] = EventSeries(**event_series_row, events=[])
            if event_series_row.get("event_id"):
                all_series[series_name].events.append(Event(**event_series_row))

        return all_series

    def get_all_series(self) -> list[EventSeries]:
        """
        Retrieves all EventSeries objects and returns them as a list.

        :raises HTTPException: If any error occurs (status code 500)
        :return list[EventSeries]: A list of EventSeries objects suitable for a response body
        """
        series_data = self.db.select_all()

        try:
            return [series for series in self._all_series(series_data).values()]
        except Exception as e:
            self.log_error(e)
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Error retrieving event objects: {e}",
            )

    def get_one_series_by_id(self, series_id: int) -> EventSeries:
        """
        Retrieves a single EventSeries object by numeric ID.

        :param int series_id: The ID of the series to retrieve
        :raises HTTPException: If the series is not found (status code 404)
        :raises HTTPException: If any error occurs during the instantiation process (status code 500)
        :return EventSeries: The EventSeries object which is suitable for a response body
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
        """
        Passes a new EventSeries object to the database for creation and returns the created object.

        :param NewEventSeries series: The new EventSeries object to create
        :raises HTTPException: If the series name already exists (status code 400)
        :return EventSeries: The created EventSeries object which is suitable for a response body
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
        """
        Updates the poster image for an EventSeries object and returns the updated object.

        :param int series_id: The numeric ID of the series
        :param UploadFile poster: The new poster image file
        :return EventSeries: The updated EventSeries object with the new poster image
        """
        series = self.get_one_series_by_id(series_id)
        series.poster_id = self._upload_poster(poster)
        self.db.update_series_poster(series)
        return self.get_one_series_by_id(series.series_id)

    def _upload_poster(self, poster: UploadFile) -> str:
        """
        Uploads an image file to the cloud and returns the public ID.

        :param UploadFile poster: The image file to upload
        :raises HTTPException: If any error occurs during the upload process (status code 500)
        :return str: The public ID of the uploaded image
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
        """
        Deletes an EventSeries object from the database.

        :param int id: The numeric ID of the series to delete
        """
        series = self.get_one_series_by_id(id)
        self.db.delete_one_series(series)

    def update_series(self, route_id: int, series: EventSeries) -> EventSeries:
        """
        Updates an EventSeries object in the database and returns the updated object.

        :param int route_id: The numeric ID in the URL
        :param EventSeries series: The updated EventSeries object
        :raises HTTPException: If the ID in the URL does not match the ID in the request body (status code 400)
        :raises HTTPException: If the poster ID is updated directly (status code 400)
        :return EventSeries: The updated EventSeries object which is suitable for a response body
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
