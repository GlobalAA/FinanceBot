from aiogram import Router

from .main import router

callbacks_router = Router()
callbacks_router.include_router(router)