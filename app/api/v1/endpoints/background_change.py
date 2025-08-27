from fastapi import (
    APIRouter,
    status,
    UploadFile,
    File,
    Form
)
from fastapi.responses import Response

from app.services.utils import replace_photo_bg


router = APIRouter()


@router.post("/bg/remove")
async def remove_bg(
    image: UploadFile = File(...),
    color: str | None = Form(None),
):
    src = await image.read()
    result_png = replace_photo_bg(src, color)
    return Response(content=result_png, media_type="image/png")
