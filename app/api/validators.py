from fastapi import (
    HTTPException,
    status,
    UploadFile,
)

from app.core.constants import (
    MAX_SIZE_EXCEEDED,
    WRONG_FILE_TYPE,
)


def validate_content_type(file: UploadFile):
    if not (file.content_type and file.content_type.startswith('image/')):
        raise HTTPException(
            status_code=status.HTTP_415_UNSUPPORTED_MEDIA_TYPE,
            detail=WRONG_FILE_TYPE,
        )


def validate_file_size(src: bytes, max_mb: int = 10):
    mb = len(src) / (1024 * 1024)
    if mb > max_mb:
        raise HTTPException(
            status_code=status.HTTP_413_REQUEST_ENTITY_TOO_LARGE,
            detail=MAX_SIZE_EXCEEDED,
        )
