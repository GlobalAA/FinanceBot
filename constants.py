from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode

from config import config
from database import BotDB

bot = Bot(
	config.BOT_TOKEN.get_secret_value(),
	default=DefaultBotProperties(parse_mode=ParseMode.HTML)
)

dp = Dispatcher()

db = BotDB()