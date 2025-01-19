from pydantic import BaseModel
from typing import Optional


class Group(BaseModel):
    name: str
    bio: str
    livestream_id: str = ""
    livestream_program_cld_id: Optional[str] = None  # not a FK! references a cloudinary ID
    id: Optional[int] = None
