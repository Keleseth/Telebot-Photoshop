import io

from fastapi import HTTPException
from PIL import Image, ImageColor
from rembg import remove

from app.core.constants import COLOR_NOT_FOUND

def replace_photo_bg(
        src_bytes: bytes,
        color: str | None
) -> bytes:
    """
    Функция вырезает фон и (опционально) заменяет на однотонный фон.
    """
    cut_png_bytes = remove(src_bytes)
    if not color:
        return cut_png_bytes

    cut = Image.open(io.BytesIO(cut_png_bytes)).convert("RGBA")
    color = color.strip().lower() if color else None
    if len(color) == 4 and color.startswith('#'):
        color = '#' + ''.join([c * 2 for c in color[1:]])
    try:
        rgb = ImageColor.getrgb(color)
    except ValueError:
        raise HTTPException(status_code=400, detail=COLOR_NOT_FOUND)
    bg = Image.new('RGBA', cut.size, rgb + (255,))
    out = Image.alpha_composite(bg, cut)
    buf = io.BytesIO()
    out.save(buf, "PNG")
    return buf.getvalue()
