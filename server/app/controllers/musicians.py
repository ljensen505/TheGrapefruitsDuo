from fastapi import HTTPException, UploadFile, status
from icecream import ic

from app.admin.images import uploader
from app.controllers.base_controller import BaseController
from app.db import musician_queries
from app.db.musicians import MusicianQueries
from app.models.musician import Musician


class MusicianController(BaseController):
    def __init__(self) -> None:
        super().__init__()
        self.db: MusicianQueries = musician_queries

    async def get_musicians(self) -> list[Musician]:
        data = await self.db.get_all()
        try:
            return [Musician(**m) for m in data]
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Error creating musician objects: {e}",
            )

    async def get_musician(self, id: int) -> Musician:
        if (data := await self.db.get_one(id)) is None:
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
        musician = await self.get_musician(musician_id)
        if new_bio != musician.bio:
            return await self.update_musician_bio(musician.id, new_bio)
        if file is not None:
            return await self.upload_headshot(musician.id, file)

        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Update operation not implemented. Neither the bio or headshot was updated.",
        )

    async def update_musician_headshot(self, id: int, headshot_id: str) -> Musician:
        await self.get_musician(id)
        try:
            await self.db.update_headshot(id, headshot_id)
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Error updating musician headshot: {e}",
            )
        return await self.get_musician(id)

    async def update_musician_bio(self, id: int, bio: str) -> Musician:
        await self.get_musician(id)  # Check if musician exists
        try:
            await self.db.update_bio(id, bio)
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Error updating musician bio: {e}",
            )
        return await self.get_musician(id)

    async def upload_headshot(self, id: int, file: UploadFile) -> Musician:
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
