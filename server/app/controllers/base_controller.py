from fastapi import HTTPException, UploadFile, status

from app.db.base_queries import BaseQueries

ALLOWED_FILES_TYPES = ["image/jpeg", "image/png"]
MAX_FILE_SIZE = 1000000  # 1 MB


class BaseController:
    def __init__(self) -> None:
        self.db: BaseQueries = None  # type: ignore
        self.ALL_FILES = ALLOWED_FILES_TYPES
        self.MAX_FILE_SIZE = MAX_FILE_SIZE

    async def verify_image(self, file: UploadFile) -> bytes:
        print("verifying image")
        if file.content_type not in self.ALL_FILES:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"File type {file.content_type} not allowed. Allowed file types are {self.ALL_FILES}",
            )
        image_file = await file.read()
        if len(image_file) > self.MAX_FILE_SIZE:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"File size {len(image_file)} bytes exceeds maximum of {self.MAX_FILE_SIZE} bytes",
            )
        return image_file
