import logging
import traceback
from datetime import datetime
from pathlib import Path

from fastapi import HTTPException, UploadFile, status
from icecream import ic

from app.constants import ALLOWED_FILES_TYPES, ONE_MB
from app.db.base_queries import BaseQueries


class BaseController:
    """
    A generic controller class which includes logging, image verification, and other common methods.
    Model-specific controllers should inherit from this class and this class should not be instantiated directly.
    """

    def __init__(self) -> None:
        self.db: BaseQueries = None  # type: ignore
        self.ALL_FILES = ALLOWED_FILES_TYPES
        self.MAX_FILE_SIZE = ONE_MB

    async def verify_image(self, file: UploadFile) -> bytes:
        """
        Verifies that the file is an image and is within the maximum file size.
        """
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

    def log_error(self, e: Exception) -> None:
        """
        Logs an error to a timestamped text file in the logs directory.
        """
        curr_dir = Path(__file__).parent
        log_dir = curr_dir / "logs"
        log_dir.mkdir(exist_ok=True)
        log_file = f"{datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}.log"
        with open(log_dir / log_file, "w") as f:
            f.write(f"{type(e)}")
            f.write("\n\n")
            f.write(str(e))
            f.write("\n\n")
            f.write(traceback.format_exc())
