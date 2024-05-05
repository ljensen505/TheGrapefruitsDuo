from datetime import datetime
from typing import Optional

from fastapi import UploadFile
from pydantic import BaseModel, HttpUrl


class Poster(BaseModel):
    """
    Represents a poster image file for an EventSeries object.
    """

    file: UploadFile


class NewEvent(BaseModel):
    """
    Represents a new event object as received from the client.
    """

    location: str
    time: datetime
    map_url: Optional[HttpUrl] = None
    ticket_url: Optional[HttpUrl] = None


class Event(NewEvent):
    """
    Represents an existing event object to be returned to the client.
    """

    event_id: int


class NewEventSeries(BaseModel):
    """
    Represents a new event series object as received from the client.
    """

    name: str
    description: str
    events: list[NewEvent]


class EventSeries(NewEventSeries):
    """
    Represents an existing event series object to be returned to the client.
    """

    series_id: int
    events: list[Event]
    poster_id: Optional[str] = None
