from typing import Optional

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
    """

    def __init__(
        self,
        event_controller: EventController = event_controller,
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
        """
        Retrieves all musicians and returns them as a list.

        :return list[Musician]: _description_
        """
        return self.musician_controller.get_musicians()

    async def get_musician(self, musician_id: int) -> Musician:
        """
        Retrieves a single musician by numeric ID.

        :param int musician_id: The ID of the musician to retrieve
        :return Musician: The musician object for a response body
        """
        return self.musician_controller.get_musician(musician_id)

    async def update_musician(
        self,
        musician: Musician,
        url_param_id: int,
        token: HTTPAuthorizationCredentials,
        file: Optional[UploadFile] = None,
    ) -> Musician:
        """
        Updates a musician in the database and returns the updated musician object.

        :param Musician musician: The musician object to update
        :param int url_param_id: The ID of the musician in the URL
        :param HTTPAuthorizationCredentials token: The OAuth token
        :param Optional[UploadFile] file: The new headshot file, defaults to None
        :raises HTTPException: If the ID in the URL does not match the ID in the request body (status code 400)
        :return Musician: The updated musician object which is suitable for a response body
        """

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
        """
        Retrieves all event series and returns them as a list.

        :return list[EventSeries]: a list of EventSeries objects for a response body
        """
        return self.event_controller.get_all_series()

    async def get_event(self, series_id: int) -> EventSeries:
        """
        Retrieves a single event series by numeric ID.

        :param int series_id: The ID of the event series to retrieve
        :return EventSeries: The event series object for a response body
        """
        return self.event_controller.get_one_series_by_id(series_id)

    async def create_event(
        self, series: NewEventSeries, token: HTTPAuthorizationCredentials
    ) -> EventSeries:
        """
        Creates a new event series and returns the created event series object.

        :param NewEventSeries series: The new event series object
        :param HTTPAuthorizationCredentials token: The OAuth token
        :return EventSeries: The newly created event series object which is suitable for a response body
        """
        _, sub = self.oauth_token.email_and_sub(token)
        self.user_controller.get_user_by_sub(sub)
        return self.event_controller.create_series(series)

    async def add_series_poster(
        self, series_id: int, poster: UploadFile, token: HTTPAuthorizationCredentials
    ) -> EventSeries:
        """
        Adds a poster to an event series and returns the updated event series object.

        :param int series_id: The ID of the event series to update
        :param UploadFile poster: The image file to upload
        :param HTTPAuthorizationCredentials token: The OAuth token
        :return EventSeries: The updated event series object which is suitable for a response body
        """
        _, sub = self.oauth_token.email_and_sub(token)
        self.user_controller.get_user_by_sub(sub)
        return self.event_controller.add_series_poster(series_id, poster)

    async def delete_series(
        self, series_id: int, token: HTTPAuthorizationCredentials
    ) -> None:
        """
        Deletes an event series by numeric ID.

        :param int series_id: The ID of the event series to delete
        :param HTTPAuthorizationCredentials token: The OAuth token
        """
        _, sub = self.oauth_token.email_and_sub(token)
        self.user_controller.get_user_by_sub(sub)
        self.event_controller.delete_series(series_id)

    async def update_series(
        self, route_id: int, series: EventSeries, token: HTTPAuthorizationCredentials
    ) -> EventSeries:
        """
        Updates an event series and returns the updated event series object.

        :param int route_id: The ID of the event series in the URL
        :param EventSeries series: The updated event series object
        :param HTTPAuthorizationCredentials token: The OAuth token
        :return EventSeries: The updated event series object which is suitable for a response body
        """
        _, sub = self.oauth_token.email_and_sub(token)
        self.user_controller.get_user_by_sub(sub)
        return self.event_controller.update_series(route_id, series)

    async def get_users(self) -> list[User]:
        """
        Retrieves all users and returns them as a list.

        :return list[User]: a list of User objects for a response body
        """
        return self.user_controller.get_users()

    async def get_user(self, user_id: int) -> User:
        """
        Retrieves a single user by numeric ID.

        :param int user_id: The ID of the user to retrieve
        :return User: The user object for a response body
        """
        return self.user_controller.get_user_by_id(user_id)

    async def create_user(self, token: HTTPAuthorizationCredentials) -> User:
        """
        Creates a new user and returns the created user object.
        Does NOT post a user to the database (this is not supported).

        :param HTTPAuthorizationCredentials token: The OAuth token
        :return User: The newly created user object which is suitable for a response body
        """
        return self.user_controller.create_user(token)

    async def get_group(self) -> Group:
        """
        Retrieves the group object and returns it.

        :return Group: The group object for a response body
        """
        return self.group_controller.get_group()

    async def update_group_bio(
        self, bio: str, token: HTTPAuthorizationCredentials
    ) -> Group:
        """
        Updates the group's bio and returns the updated group object.

        :param str bio: The new bio for the group
        :param HTTPAuthorizationCredentials token: The OAuth token
        :return Group: The updated group object which is suitable for a response body
        """
        _, sub = self.oauth_token.email_and_sub(token)
        self.user_controller.get_user_by_sub(sub)
        return self.group_controller.update_group_bio(bio)
