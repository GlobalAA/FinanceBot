import asyncio
import logging

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from tortoise import Tortoise

from app.callbacks import callbacks_router
from app.config import config
from app.handlers import setup_router

logging.basicConfig(level=logging.INFO)

async def main_async():
	bot = Bot(
		config.BOT_TOKEN.get_secret_value(),
		default=DefaultBotProperties(parse_mode=ParseMode.HTML)
	)
	dp = Dispatcher()

	await Tortoise.init(
		db_url=config.DB_URL.get_secret_value(),
		modules={'models': ['app.models.models']}
	)

	
	dp.include_router(setup_router())
	dp.include_router(callbacks_router)

	await bot.delete_webhook(True)
	await dp.start_polling(bot)

if __name__ == "__main__":
	try:
		asyncio.run(main_async())
	except KeyboardInterrupt:
		...