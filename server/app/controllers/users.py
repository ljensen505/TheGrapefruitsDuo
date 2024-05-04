from fastapi import HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials

from app.admin import oauth_token
from app.controllers.base_controller import BaseController
from app.db import user_queries
from app.db.users import UserQueries
from app.models.user import User


class UserController(BaseController):
    """
    Handles all user-related operations and serves as an intermediate controller between
    the main controller and the model layer.

    Inherits from BaseController, which provides logging and other generic methods.

    Testing: pass a mocked UserQueries object to the constructor.
    """

    def __init__(self, user_queries=user_queries) -> None:
        super().__init__()
        self.db: UserQueries = user_queries

    def get_users(self) -> list[User]:
        """Retrieves all users from the database and returns them as a list of User objects.

        Raises:
            HTTPException: If any error occurs during the retrieval process (status code 500)

        Returns:
            list[User]: A list of User objects which are suitable for a response body
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
        """Retrieves a single user from the database and returns it as a User object.

        Args:
            user_id (int): The ID of the user to retrieve

        Raises:
            HTTPException: If the user is not found (status code 404)
            HTTPException: If any error occurs during the retrieval process (status code 500)

        Returns:
            User: A User object which is suitable for a response body
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
        """Retrieves a single user from the database and returns it as a User object.

        Args:
            email (str): The email of the user to retrieve

        Raises:
            HTTPException: If the user is not found (status code 404)
            HTTPException: If any error occurs during the retrieval process (status code 500)

        Returns:
            User: A User object which is suitable for a response body
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
        """Retrieves a single user from the database and returns it as a User object.

        Args:
            sub (str): The sub of the user to retrieve

        Raises:
            HTTPException: If the user is not found (status code 404)
            HTTPException: If any error occurs during the retrieval process (status code 500)

        Returns:
            User: A User object which is suitable for a response body
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
        """Updates a user's sub in the database and creates a new User object.

        Args:
            token (HTTPAuthorizationCredentials): The token containing the user's email and sub

        Returns:
            User: A User object which is suitable for a response body
        """
        email, sub = oauth_token.email_and_sub(token)
        user: User = self.get_user_by_email(email)
        if user.sub is None:
            self.db.update_sub(user.email, sub)
        return self.get_user_by_sub(sub)
