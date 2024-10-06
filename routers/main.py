from aiogram import Router
from aiogram.filters import Command, CommandObject, CommandStart
from aiogram.types import Message
from aiogram.utils.keyboard import InlineKeyboardBuilder

from callbacks.models import ActionData, ActionType, WithinType
from constants import db
from middlewares import RegisterMiddleware

router = Router(name="main_router")
router.message.middleware(RegisterMiddleware())

@router.message(CommandStart())
async def start_command(message: Message):
	await message.reply("""										 
	Привіт, я ваш бот для фінансового обліку (гривня, в якості основної валюти). 💰
										 
Надішліть мені /spend, щоб додати витрати 
Надішліть мені /earn, щоб додати дохід 
Надішліть мені /all, щоб отримати всі доходи та витрати
	""")

@router.message(Command("spend"))
@router.message(Command("earn"))
async def spend_earn_command(message: Message, command: CommandObject):
	args = command.args.split(" ")
	amount = float(args[0])

	if not db.get_user(message.from_user.id):
		return await message.reply("Ви не зареєстровані. Сталася помилка, будь-ласка повідомте адміністратора")

	db.add_transaction(message.from_user.id, amount, command.command == "earn")
	return await message.reply(f"Додано {amount} до ваших {'доходів' if command.command == 'earn' else 'витрат'}")

@router.message(Command("all"))
async def all_command(message: Message, command: CommandObject):
	if not db.get_user(message.from_user.id):
		return await message.reply("Ви не зареєстровані. Сталася помилка, будь-ласка повідомте адміністратора")

	within = "*"
	if (args := command.args) != None:
		args = args.split(" ")
		within = args[0].lower()

	if not within in ["day", "month", "*"]:
		return await message.reply("Некоректно викликана команда. Використовуйте /all <day/month>")
	
	transactions = db.get_transactions(message.from_user.id, within)

	builder = InlineKeyboardBuilder()
	builder.button(
		text="Назад",
		callback_data=ActionData(id=0, action=ActionType.back, within=within).pack()
	)
	builder.button(
		text="Далі",
		callback_data=ActionData(id=0, action=ActionType.next, within=within).pack()
	)
	builder.adjust(2)

	texts = f"<b>Список доходів і витрат за {'останній день' if within == 'day' else 'весь час' if within == '*' else 'останній місяць'}</b>\n\n"
	for transaction in transactions[:10]:
		texts += f"{'➕' if transaction.profit else '➖'} <b>{transaction.amount}</b>грн ({transaction.date})\n"
	
	return await message.reply(texts, reply_markup=builder.as_markup())