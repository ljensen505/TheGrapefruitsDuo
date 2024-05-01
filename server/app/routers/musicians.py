from fastapi import APIRouter, Depends, UploadFile, status
from fastapi.security import HTTPAuthorizationCredentials
from icecream import ic

from app.admin import oauth2_http
from app.controllers import controller
from app.models.musician import Musician

router = APIRouter(
    prefix="/musicians",
    tags=["musicians"],
    responses={404: {"description": "Not found"}},
)


@router.get("/", status_code=status.HTTP_200_OK)
async def get_musicians() -> list[Musician]:
    return await controller.get_musicians()


@router.get("/{id}", status_code=status.HTTP_200_OK)
async def get_musician(id: int) -> Musician:
    return await controller.get_musician(id)


@router.patch("/{id}")
async def update_musician(
    id: int,
    musician: Musician,
    token: HTTPAuthorizationCredentials = Depends(oauth2_http),
) -> Musician:
    """Updates a musician's bio, but requires the entire musician object to be sent in the request body.
    Requires authentication."""
    return await controller.update_musician(
        musician=musician, url_param_id=id, token=token
    )


@router.post("/{id}/headshot", status_code=status.HTTP_200_OK)
async def update_musician_headshot(
    id: int,
    file: UploadFile,
    token: HTTPAuthorizationCredentials = Depends(oauth2_http),
) -> Musician | None:
    """Recieves a headshot image file, uploads it to cloudinary, and updates the musician's headshot url in the database"""
    musician = await controller.get_musician(id)
    return await controller.update_musician(
        musician=musician, url_param_id=id, token=token, file=file
    )
