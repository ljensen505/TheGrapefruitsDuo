from fastapi import HTTPException, UploadFile, status
from fastapi.security import HTTPAuthorizationCredentials
from icecream import ic

from app.admin import oauth_token
from app.controllers import (
    event_controller,
    group_controller,
    musicians_controller,
    user_controller,
)
from app.controllers.events import EventController
from app.controllers.group import GroupController
from app.controllers.musicians import MusicianController
from app.controllers.users import UserController
from app.models.event import EventSeries, NewEventSeries
from app.models.group import Group
from app.models.musician import Musician
from app.models.user import User


class MainController:
    """
    The main controller and entry point for all API requests.
    All methods are either pass-throughs to the appropriate controller or
    are used to coordinate multiple controllers.

    All methods are asynchronous to facilitate asynchronous calls from the Router layer.

    token-based authentication is handled here as needed per the nature of the data being accessed.

    Testing: pass mocked sub-controllers to the constructor.
    """

    def __init__(
        self,
        event_controller=event_controller,
        musicians_controller=musicians_controller,
        user_controller=user_controller,
        group_controller=group_controller,
        oauth_token=oauth_token,
    ) -> None:
        self.event_controller = event_controller
        self.musician_controller = musicians_controller
        self.user_controller = user_controller
        self.group_controller = group_controller
        self.oauth_token = oauth_token

    async def get_musicians(self) -> list[Musician]:
        return self.musician_controller.get_musicians()

    async def get_musician(self, musician_id: int) -> Musician:
        return self.musician_controller.get_musician(musician_id)

    async def update_musician(
        self,
        musician: Musician,
        url_param_id: int,
        token: HTTPAuthorizationCredentials,
        file: UploadFile | None = None,
    ) -> Musician:

        if musician.id != url_param_id:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="ID in URL does not match ID in request body",
            )
        _, sub = self.oauth_token.email_and_sub(token)
        self.user_controller.get_user_by_sub(sub)
        return self.musician_controller.update_musician(
            musician_id=musician.id,
            new_bio=musician.bio,
            file=file,
        )

    async def get_events(self) -> list[EventSeries]:
        return self.event_controller.get_all_series()

    async def get_event(self, series_id: int) -> EventSeries:
        return self.event_controller.get_one_series_by_id(series_id)

    async def create_event(
        self, series: NewEventSeries, token: HTTPAuthorizationCredentials
    ) -> EventSeries:
        _, sub = self.oauth_token.email_and_sub(token)
        self.user_controller.get_user_by_sub(sub)
        return self.event_controller.create_series(series)

    async def add_series_poster(
        self, series_id: int, poster: UploadFile, token: HTTPAuthorizationCredentials
    ) -> EventSeries:
        _, sub = self.oauth_token.email_and_sub(token)
        self.user_controller.get_user_by_sub(sub)
        return self.event_controller.add_series_poster(series_id, poster)

    async def delete_series(
        self, series_id: int, token: HTTPAuthorizationCredentials
    ) -> None:
        _, sub = self.oauth_token.email_and_sub(token)
        self.user_controller.get_user_by_sub(sub)
        self.event_controller.delete_series(series_id)

    async def update_series(
        self, route_id: int, series: EventSeries, token: HTTPAuthorizationCredentials
    ) -> EventSeries:
        _, sub = self.oauth_token.email_and_sub(token)
        self.user_controller.get_user_by_sub(sub)
        return self.event_controller.update_series(route_id, series)

    async def get_users(self) -> list[User]:
        return self.user_controller.get_users()

    async def get_user(self, user_id: int) -> User:
        return self.user_controller.get_user_by_id(user_id)

    async def create_user(self, token: HTTPAuthorizationCredentials) -> User:
        """This method does NOT post a user to the database.
        Instead, it retrieves the user's information from the OAuth token,
        updates the user's sub in the db if needed, and returns the user object.

        Args:
            token (HTTPAuthorizationCredentials): The OAuth token

        Returns:
            User: The User object
        """
        return self.user_controller.create_user(token)

    async def get_group(self) -> Group:
        return self.group_controller.get_group()

    async def update_group_bio(
        self, bio: str, token: HTTPAuthorizationCredentials
    ) -> Group:
        _, sub = self.oauth_token.email_and_sub(token)
        self.user_controller.get_user_by_sub(sub)
        return self.group_controller.update_group_bio(bio)
