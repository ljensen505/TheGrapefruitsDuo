from fastapi import HTTPException, status

from app.controllers.base_controller import BaseController
from app.db import group_queries
from app.db.group import GroupQueries
from app.models.group import Group


class GroupController(BaseController):
    def __init__(self) -> None:
        super().__init__()
        self.db: GroupQueries = group_queries

    async def get_group(self) -> Group:
        if (data := await self.db.select_one_by_id()) is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Group not found"
            )
        try:
            return Group(**data)
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Error creating group object: {e}",
            )

    async def update_group_bio(self, bio: str) -> Group:
        try:
            await self.db.update_group_bio(bio)
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Error updating group bio: {e}",
            )
        return await self.get_group()
