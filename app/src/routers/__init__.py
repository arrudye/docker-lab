from .books import router as books_router
from .readers import router as readers_router
from .loans import router as loans_router

__all__ = ['books_router', 'readers_router', 'loans_router']