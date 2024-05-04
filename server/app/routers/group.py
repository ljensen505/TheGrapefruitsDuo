from fastapi import APIRouter, Depends, status
from fastapi.security.http import HTTPAuthorizationCredentials
from icecream import ic

from app.admin import oauth2_http
from app.models.group import Group
from app.routers import controller

router = APIRouter(
    prefix="/group",
    tags=["group"],
    responses={404: {"description": "Not found"}},
)


@router.get("/", status_code=status.HTTP_200_OK)
async def get_group() -> Group:
    return await controller.get_group()


@router.patch("/")
async def update_group(
    group: Group, token: HTTPAuthorizationCredentials = Depends(oauth2_http)
) -> Group:
    """Updates the group bio, but requires the entire group object to be sent in the request body.
    Requires authentication."""
    return await controller.update_group_bio(group.bio, token)
