from datetime import datetime
from typing import Optional

from fastapi import UploadFile
from pydantic import BaseModel, HttpUrl


class Poster(BaseModel):
    file: UploadFile


class NewEvent(BaseModel):
    location: str
    time: datetime
    map_url: Optional[HttpUrl] = None
    ticket_url: Optional[HttpUrl] = None


class Event(NewEvent):
    event_id: int


class NewEventSeries(BaseModel):
    name: str
    description: str
    events: list[NewEvent]


class EventSeries(NewEventSeries):
    series_id: int
    events: list[Event]
    poster_id: Optional[str] = None
