from fastapi import HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials

from app.admin import oauth_token
from app.controllers.base_controller import BaseController
from app.db import user_queries
from app.db.users import UserQueries
from app.models.user import User


class UserController(BaseController):
    def __init__(self) -> None:
        super().__init__()
        self.db: UserQueries = user_queries

    async def get_users(self) -> list[User]:
        data = await self.db.select_all_series()
        try:
            return [User(**e) for e in data]
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Error creating user objects: {e}",
            )

    async def get_user_by_id(self, id: int) -> User:
        if (data := await self.db.select_one_series_by_id(id)) is None:
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

    async def get_user_by_email(self, email: str) -> User:
        if (data := await self.db.get_one_by_email(email)) is None:
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

    async def get_user_by_sub(self, sub: str) -> User:
        if (data := await self.db.get_one_by_sub(sub)) is None:
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

    async def create_user(self, token: HTTPAuthorizationCredentials) -> User:
        email, sub = oauth_token.email_and_sub(token)
        user: User = await self.get_user_by_email(email)
        if user.sub is None:
            await self.db.update_sub(user.email, sub)
        return await self.get_user_by_sub(sub)
