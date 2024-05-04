from fastapi import HTTPException, status

from app.controllers.base_controller import BaseController
from app.db import group_queries
from app.db.group import GroupQueries
from app.models.group import Group


class GroupController(BaseController):
    """
    Handles all group-related operations and serves as an intermediate controller between
    the main controller and the model layer.
    Inherits from BaseController, which provides logging and other generic methods.

    The corresponding table contains only one row.

    Testing: pass a mocked GroupQueries object to the constructor.
    """

    def __init__(self, group_queries=group_queries) -> None:
        super().__init__()
        self.group_queries: GroupQueries = group_queries

    def get_group(self) -> Group:
        """Retrieves the group from the database and returns it as a Group object.

        Raises:
            HTTPException: If the group is not found (status code 404)
            HTTPException: If any error occurs during the retrieval process (status code 500)

        Returns:
            Group: A Group object which is suitable for a response body
        """
        if (data := self.group_queries.select_one_by_id()) is None:
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

    def update_group_bio(self, bio: str) -> Group:
        """Updates the group's bio in the database and returns the updated Group object.

        Args:
            bio (str): The new bio for the group

        Raises:
            HTTPException: If any error occurs during the update process (status code 500)

        Returns:
            Group: The updated Group object which is suitable for a response body
        """
        try:
            self.group_queries.update_group_bio(bio)
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Error updating group bio: {e}",
            )
        return self.get_group()
