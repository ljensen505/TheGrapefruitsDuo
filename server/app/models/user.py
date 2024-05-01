from typing import Optional

from pydantic import BaseModel


class User(BaseModel):
    name: str
    email: str
    sub: Optional[str] = None
    id: int | None = None


USER_TABLE = "users"
