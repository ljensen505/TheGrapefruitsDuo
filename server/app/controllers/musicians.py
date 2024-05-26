from typing import Optional

from fastapi import HTTPException, UploadFile, status
from icecream import ic

from app.admin.images import uploader
from app.controllers.base_controller import BaseController
from app.db import musician_queries
from app.db.musicians import MusicianQueries
from app.models.musician import Musician


class MusicianController(BaseController):
    """
    Handles all musician-related operations.
    Inherits from BaseController, which provides logging and other generic methods.
    """

    def __init__(self, musician_queries: MusicianQueries = musician_queries) -> None:
        """
        Initializes the MusicianController with a MusicianQueries object.

        :param MusicianQueries musician_queries: object for querying musician data, defaults to musician_queries
        """
        super().__init__()
        self.db: MusicianQueries = musician_queries

    def get_musicians(self) -> list[Musician]:
        """
        Retrieves all musicians and returns them as a list.

        :raises HTTPException: If any error occurs during the retrieval process (status code 500)
        :return list[Musician]: A list of Musician objects suitable for a response body
        """
        data = self.db.select_all()
        try:
            return [Musician(**m) for m in data]
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Error creating musician objects: {e}",
            )

    def get_musician(self, musician_id: int) -> Musician:
        """
        Retrieves a single musician by numeric ID.

        :param int musician_id: The ID of the musician to retrieve
        :raises HTTPException: If the musician is not found (status code 404)
        :raises HTTPException: If any error occurs during the instantiation process (status code 500)
        :return Musician: The musician object for a response body
        """
        if (data := self.db.select_one_by_id(musician_id)) is None:
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

    def update_musician(
        self,
        musician_id: int,
        new_bio: str,
        file: Optional[UploadFile] = None,
    ) -> Musician:
        """
        Updates a musician in the database and returns the updated musician object.

        :param int musician_id: The ID of the musician to update
        :param str new_bio: The new biography for the musician
        :param Optional[UploadFile] file: The new headshot file, defaults to None
        :raises HTTPException: _description_
        :return Musician: _description_
        """
        musician = self.get_musician(musician_id)
        if new_bio != musician.bio:
            return self._update_musician_bio(musician, new_bio)
        if file is not None:
            return self._upload_headshot(musician, file)

        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Update operation not implemented. Neither the bio or headshot was updated.",
        )

    def _update_musician_headshot(
        self, musician: Musician, headshot_id: str
    ) -> Musician:
        """
        Updates a musician's headshot in the database.

        :param Musician musician: The musician object to update
        :param str headshot_id: The new public ID for the headshot
        :raises HTTPException: If any error occurs during the update process (status code 500)
        :return Musician: The updated Musician object
        """
        try:
            self.db.update_headshot(musician, headshot_id)
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Error updating musician headshot: {e}",
            )
        return self.get_musician(musician.id)

    def _update_musician_bio(self, musician: Musician, bio: str) -> Musician:
        """
        Updates a musician's biography in the database.

        :param Musician musician: The musician object to update
        :param str bio: The new biography for the musician
        :raises HTTPException: If any error occurs during the update process (status code 500)
        :return Musician: The updated Musician object
        """
        try:
            self.db.update_bio(musician, bio)
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Error updating musician bio: {e}",
            )
        return self.get_musician(musician.id)

    def _upload_headshot(self, musician: Musician, file: UploadFile) -> Musician:
        """
        Uploads a new headshot image for a musician and returns the updated musician object.

        :param Musician musician: The musician object to update
        :param UploadFile file: The new headshot file
        :raises HTTPException: If any error occurs during the upload process (status code 500)
        :return Musician: The updated Musician object
        """
        image_file = self.verify_image(file)
        data = uploader.upload(image_file)
        public_id = data.get("public_id")
        if public_id is None:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Failed to upload image",
            )
        self._update_musician_headshot(musician, public_id)

        return self.get_musician(musician.id)
