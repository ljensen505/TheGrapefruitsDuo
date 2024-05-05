from fastapi import HTTPException, status

from app.controllers.base_controller import BaseController
from app.db import group_queries
from app.db.group import GroupQueries
from app.models.group import Group


class GroupController(BaseController):
    """
    Handles all group-related operations.
    Inherits from BaseController, which provides logging and other generic methods.
    """

    def __init__(self, group_queries=group_queries) -> None:
        """
        Initializes the GroupController with a GroupQueries object.

        :param GroupQueries group_queries: object for quering group data, defaults to group_queries
        """
        super().__init__()
        self.group_queries: GroupQueries = group_queries

    def get_group(self) -> Group:
        """
        Instantiates a Group object and retuns it for a response body.

        :raises HTTPException: If the group is not found (status code 404)
        :raises HTTPException: If any error occurs during the instantiation process (status code 500)
        :return Group: The Group object which is suitable for a response body
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
        """
        Updates the group's bio in the database and returns the updated Group object.

        :param str bio: The new bio for the group
        :raises HTTPException: If any error occurs during the update process (status code 500)
        :return Group: The updated Group object which is suitable for a response body
        """
        try:
            self.group_queries.update_group_bio(bio)
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Error updating group bio: {e}",
            )
        return self.get_group()
