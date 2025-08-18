from .start import router as start_router
from .photos.photos import router as incoming_photos_router
from .photos.photos_remove_bg import router as remove_photos_bg_router


__all__ = [
    'start_router',
    'incoming_photos_router',
    'remove_photos_bg_router',
]
