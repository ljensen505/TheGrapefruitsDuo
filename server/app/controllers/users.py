from fastapi import HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials

from app.admin import oauth_token
from app.controllers.base_controller import BaseController
from app.db import user_queries
from app.db.users import UserQueries
from app.models.user import User


class UserController(BaseController):
    """
    Handles all user-related operations.
    Inherits from BaseController, which provides logging and other generic methods.
    """

    def __init__(self, user_queries: UserQueries = user_queries) -> None:
        """
        Initializes the UserController with a UserQueries object.

        :param UserQueries user_queries: object for querying user data, defaults to user_queries
        """
        super().__init__()
        self.db: UserQueries = user_queries

    def get_users(self) -> list[User]:
        """
        Retrieves all users and returns them as a list.

        :raises HTTPException: If any error occurs during the retrieval process (status code 500)
        :return list[User]: A list of User objects suitable for a response body
        """
        data = self.db.select_all_series()
        try:
            return [User(**e) for e in data]
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Error creating user objects: {e}",
            )

    def get_user_by_id(self, user_id: int) -> User:
        """
        Retrieves a single user from the database and returns it as a User object.

        :param int user_id: The ID of the user to retrieve
        :raises HTTPException: If the user is not found (status code 404)
        :raises HTTPException: If any error occurs during the retrieval process (status code 500)
        :return User: A User object which is suitable for a response body
        """
        if (data := self.db.select_one_by_id(user_id)) is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
            )
        try:
            return User(**data)
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Error creating user object: {e}",
            )

    def get_user_by_email(self, email: str) -> User:
        """
        Retrieves a single user from the database and returns it as a User object.

        :param str email: The email of the user to retrieve
        :raises HTTPException: If the user is not found (status code 404)
        :raises HTTPException: If any error occurs during the retrieval process (status code 500)
        :return User: A User object which is suitable for a response body
        """
        if (data := self.db.select_one_by_email(email)) is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="User does not exist"
            )
        try:
            return User(**data)
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Error creating user object: {e}",
            )

    def get_user_by_sub(self, sub: str) -> User:
        """
        Retrieves a single user from the database and returns it as a User object.

        :param str sub: The sub of the user to retrieve
        :raises HTTPException: If the user is not found (status code 404)
        :raises HTTPException: If any error occurs during the retrieval process (status code 500)
        :return User: A User object which is suitable for a response body
        """
        if (data := self.db.select_one_by_sub(sub)) is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
            )
        try:
            return User(**data)
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Error creating user object: {e}",
            )

    def create_user(self, token: HTTPAuthorizationCredentials) -> User:
        """
        Creates a new user in the database and returns the created User object.

        :param HTTPAuthorizationCredentials token: The OAuth token
        :return User: The created User object which is suitable for a response body
        """
        email, sub = oauth_token.email_and_sub(token)
        user: User = self.get_user_by_email(email)
        if user.sub is None:
            self.db.update_sub(user.email, sub)
        return self.get_user_by_sub(sub)
