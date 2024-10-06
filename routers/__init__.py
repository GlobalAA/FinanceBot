from aiogram import Router

from .main import router as main_router

init_router = Router(name="init_router")
init_router.include_router(main_router)