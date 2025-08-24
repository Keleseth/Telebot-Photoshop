from fastapi import (
    APIRouter,
    status,
    UploadFile,
    File
)
from fastapi.responses import StreamingResponse
from rembg import remove
from PIL import Image
import io


router = APIRouter()


@router.post(
    '/bg/remove',
    status_code=status.HTTP_200_OK
)
async def remove_bg(
    file: UploadFile = File(...)
):
    contents = await file.read()
    result = remove(contents)
    img = Image.open(io.BytesIO(result)).convert("RGBA")
    buf = io.BytesIO()
    img.save(buf, format="PNG")
    buf.seek(0)
    response = StreamingResponse(buf, media_type="image/png")
    return response
