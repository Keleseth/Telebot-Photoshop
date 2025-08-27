import io
from PIL import Image, ImageColor
from rembg import remove


def replace_photo_bg(
        src_bytes: bytes,
        color: str | None
) -> bytes:
    cut_png_bytes = remove(src_bytes)
    if not color:
        return cut_png_bytes

    cut = Image.open(io.BytesIO(cut_png_bytes)).convert("RGBA")
    W, H = cut.size
    rgb = ImageColor.getrgb(color)
    bg = Image.new("RGBA", (W, H), rgb + (255,))
    out = Image.alpha_composite(bg, cut)
    buf = io.BytesIO()
    out.save(buf, "PNG")
    return buf.getvalue()
