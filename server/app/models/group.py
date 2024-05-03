from pydantic import BaseModel


class Group(BaseModel):
    name: str
    bio: str
    id: int | None = None
