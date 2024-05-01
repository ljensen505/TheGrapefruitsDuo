from pydantic import BaseModel

from app.models.event import EventSeries
from app.models.group import Group
from app.models.musician import Musician


class TheGrapefruitsDuo(BaseModel):
    version: str
    group: Group
    musicians: list[Musician]
    events: list[EventSeries]
