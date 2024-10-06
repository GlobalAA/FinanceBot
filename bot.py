import logging
from asyncio import run

from routers import init_router

logging.basicConfig(level=logging.INFO)
from callbacks import callbacks_router
from constants import bot, dp


@dp.startup()
async def on_startup():
	await bot.delete_webhook(drop_pending_updates=True)

async def main():
	dp.include_routers(init_router)
	dp.include_routers(callbacks_router)
	await dp.start_polling(bot)

if __name__ == "__main__":
	try:
		run(main())
	except RuntimeError:
		...