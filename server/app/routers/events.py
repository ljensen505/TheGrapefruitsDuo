from fastapi import APIRouter, Depends, File, UploadFile
from fastapi.security import HTTPAuthorizationCredentials
from icecream import ic

from app.admin import oauth2_http
from app.controllers import controller
from app.models.event import EventSeries, NewEventSeries

router = APIRouter(
    prefix="/events",
    tags=["events"],
    responses={404: {"description": "Not found"}},
)


@router.get("/")
async def get_events() -> list[EventSeries]:
    return await controller.get_events()


@router.get("/{id}")
async def get_event(id: int) -> EventSeries:
    return await controller.get_event(id)


@router.post("/")
async def create_series(
    series: NewEventSeries,
    token: HTTPAuthorizationCredentials = Depends(oauth2_http),
) -> EventSeries:
    return await controller.create_event(series, token)


@router.delete("/{id}")
async def delete_event(
    id: int, token: HTTPAuthorizationCredentials = Depends(oauth2_http)
) -> None:
    await controller.delete_series(id, token)


@router.post("/{id}/poster")
async def add_series_poster(
    id: int,
    poster: UploadFile = File(...),
    token: HTTPAuthorizationCredentials = Depends(oauth2_http),
) -> EventSeries:
    return await controller.add_series_poster(id, poster, token)


@router.put("/{id}")
async def update_event(
    id: int,
    event: EventSeries,
    token: HTTPAuthorizationCredentials = Depends(oauth2_http),
) -> EventSeries:
    return await controller.update_series(id, event, token)
