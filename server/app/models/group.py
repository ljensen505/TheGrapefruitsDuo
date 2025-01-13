from pydantic import BaseModel
from typing import Optional


class Group(BaseModel):
    name: str
    bio: str
    livestream_id: str = ""
    id: Optional[int] = None
