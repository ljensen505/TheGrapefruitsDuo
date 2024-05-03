from fastapi import APIRouter, Depends, status
from fastapi.security import HTTPAuthorizationCredentials

from app.admin import oauth2_http
from app.controllers import controller
from app.models.user import User

router = APIRouter(
    prefix="/users",
    tags=["users"],
    responses={404: {"description": "Not found"}},
)


"""
Note: this router is not currently registered in the main FastAPI app.
This is to facilitate not exposing the user routes to the public API,
but this may change in a future version.

The file remains to ease the future addition of user routes.
"""


@router.get("/", status_code=status.HTTP_200_OK)
async def get_users() -> list[User]:
    return await controller.get_users()


@router.get("/{id}", status_code=status.HTTP_200_OK)
async def get_user(id: int) -> User:
    return await controller.get_user(id)


@router.post("/", status_code=status.HTTP_200_OK)
async def create_user(
    token: HTTPAuthorizationCredentials = Depends(oauth2_http),
) -> User | None:
    return await controller.create_user(token)
