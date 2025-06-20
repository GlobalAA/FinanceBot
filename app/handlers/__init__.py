from aiogram import Router

from . import finance


def setup_router() -> Router:
	router = Router()

	router.include_router(finance.router)

	return router