from fastapi import (
    APIRouter,
    File,
    Form,
    HTTPException,
    UploadFile,
)
from fastapi.responses import Response
from starlette.concurrency import run_in_threadpool

from app.api.validators import (
    validate_content_type,
    validate_file_size
)
from app.core.constants import (
    COLOR_NOT_FOUND,
    IMAGE_MAX_WEIGHT,
)
from app.services.utils import replace_photo_bg


router = APIRouter(
    prefix='/bg',
    tags=['background']
)


@router.post('/remove')
async def remove_bg(
    image: UploadFile = File(...),
    color: str | None = Form(None),
):
    validate_content_type(file=image)
    src = await image.read()
    validate_file_size(
        src=src,
        max_mb=IMAGE_MAX_WEIGHT
    )
    try:
        result_png = await run_in_threadpool(replace_photo_bg, src, color)
    except ValueError:
        raise HTTPException(
            status_code=400,
            detail=COLOR_NOT_FOUND
        )
    return Response(content=result_png, media_type='image/png')
