from .start import router as start_router
from .photos.photos import router as incoming_photos_router
from .admin_zone.whitelist import wl_handle_router
from .photos.photos_remove_bg import (
    rm_bg_router,
    bg_color_change_router,
)


__all__ = [
    'start_router',
    'incoming_photos_router',
    'rm_bg_router',
    'bg_color_change_router',
    'wl_handle_router'
]
