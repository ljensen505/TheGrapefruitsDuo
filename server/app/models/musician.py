from typing import Optional

from pydantic import BaseModel, Field


class NewMusician(BaseModel):
    name: str
    bio: str
    headshot_id: str  # cloudinary id


class Musician(NewMusician):
    id: int


MUSICIAN_TABLE = "musicians"
