from fastapi import HTTPException, UploadFile, status
from icecream import ic

from app.admin.images import uploader
from app.controllers.base_controller import BaseController
from app.db import musician_queries
from app.db.musicians import MusicianQueries
from app.models.musician import Musician


class MusicianController(BaseController):
    """
    Handles all musician-related operations and serves as an intermediate controller between
    the main controller and the model layer.
    Inherits from BaseController, which provides logging and other generic methods.

    Testing: pass a mocked MusicianQueries object to the constructor.
    """

    def __init__(self, musician_queries=musician_queries) -> None:
        super().__init__()
        self.db: MusicianQueries = musician_queries

    async def get_musicians(self) -> list[Musician]:
        """Retrieves all musicians from the database and returns them as a list of Musician objects.

        Raises:
            HTTPException: If any error occurs during the retrieval process (status code 500)

        Returns:
            list[Musician]: A list of Musician objects which are suitable for a response body
        """
        data = await self.db.select_all_series()
        try:
            return [Musician(**m) for m in data]
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Error creating musician objects: {e}",
            )

    async def get_musician(self, musician_id: int) -> Musician:
        """Retrieves a single musician from the database and returns it as a Musician object.

        Args:
            id (int): The ID of the musician to retrieve

        Raises:
            HTTPException: If the musician is not found (status code 404)
            HTTPException: If any error occurs during the retrieval process (status code 500)

        Returns:
            Musician: A Musician object which is suitable for a response body
        """
        if (data := await self.db.select_one_by_id(musician_id)) is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Musician not found"
            )
        try:
            return Musician(**data)
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Error creating musician object: {e}",
            )

    async def update_musician(
        self,
        musician_id: int,
        new_bio: str,
        file: UploadFile | None = None,
    ) -> Musician:
        """Updates a musician's bio and/or headshot by conditionally calling the appropriate methods.

        Args:
            musician_id (int): The numeric ID of the musician to update
            new_bio (str): The new biography for the musician
            file (UploadFile | None, optional): The new headshot file. Defaults to None.

        Raises:
            HTTPException: If the musician is not found (status code 404)

        Returns:
            Musician: The updated Musician object
        """
        musician = await self.get_musician(musician_id)
        if new_bio != musician.bio:
            return await self._update_musician_bio(musician.id, new_bio)
        if file is not None:
            return await self._upload_headshot(musician.id, file)

        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Update operation not implemented. Neither the bio or headshot was updated.",
        )

    async def update_musician_headshot(
        self, musician_id: int, headshot_id: str
    ) -> Musician:
        """Updates a musician's headshot in the database.

        Args:
            id (int): The numeric ID of the musician to update
            headshot_id (str): The public ID of the new headshot (as determined by Cloudinary)

        Raises:
            HTTPException: If any error occurs during the update process (status code 500)

        Returns:
            Musician: The updated Musician object
        """
        await self.get_musician(musician_id)
        try:
            await self.db.update_headshot(musician_id, headshot_id)
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Error updating musician headshot: {e}",
            )
        return await self.get_musician(musician_id)

    async def _update_musician_bio(self, musician_id: int, bio: str) -> Musician:
        """Updates a musician's bio in the database.

        Args:
            id (int): The numeric ID of the musician to update
            bio (str): The new biography for the musician

        Raises:
            HTTPException: If any error occurs during the update process (status code 500)

        Returns:
            Musician: The updated Musician object
        """
        await self.get_musician(musician_id)  # Check if musician exists
        try:
            await self.db.update_bio(musician_id, bio)
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Error updating musician bio: {e}",
            )
        return await self.get_musician(musician_id)

    async def _upload_headshot(self, id: int, file: UploadFile) -> Musician:
        """Uploads a new headshot for a musician and updates the database with the new public ID.

        Args:
            id (int): The numeric ID of the musician to update
            file (UploadFile): The new headshot file

        Raises:
            HTTPException: If the file is not an image or exceeds the maximum file size (status code 400)

        Returns:
            Musician: The updated Musician object
        """
        image_file = await self.verify_image(file)
        data = uploader.upload(image_file)
        public_id = data.get("public_id")
        if public_id is None:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Failed to upload image",
            )
        await self.update_musician_headshot(id, public_id)

        return await self.get_musician(id)
