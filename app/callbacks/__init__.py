from aiogram import Router

from .statistics import router as st_router
from .transactions import router as tr_router

callbacks_router = Router()
callbacks_router.include_router(tr_router)
callbacks_router.include_router(st_router)