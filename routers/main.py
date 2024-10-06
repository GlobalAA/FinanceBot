from aiogram import Router
from aiogram.filters import Command, CommandObject, CommandStart
from aiogram.types import Message

from constants import db
from middlewares import RegisterMiddleware

router = Router(name="main_router")
router.message.middleware(RegisterMiddleware())

@router.message(CommandStart())
async def start_command(message: Message):
	await message.reply("""
	Hi, I am your bot for financial accounting.

Send me /spend to add an expense 
Send me /earn to add income 
Send me /all to get all income and expenses
	""")

@router.message(Command("spend"))
@router.message(Command("earn"))
async def spend_earn_command(message: Message, command: CommandObject):
	args = command.args.split(" ")
	amount = float(args[0])

	if not db.get_user(message.from_user.id):
		return await message.reply("You are not registered. Report an error to the administrator")

	db.add_transaction(message.from_user.id, amount, command.command == "earn")
	return await message.reply(f"Added {amount} to your {'earnings' if command.command == 'earn' else 'expenses'}")

@router.message(Command("all"))
async def all_command(message: Message, command: CommandObject):
	if not db.get_user(message.from_user.id):
		return await message.reply("You are not registered. Report an error to the administrator")

	within = "*"
	if (args := command.args) != None:
		args = args.split(" ")
		within = args[0].lower()

	if not within in ["day", "month", "*"]:
		return await message.reply("Invalid argument. Use /all <day/month>")
	
	transactions = db.get_transactions(message.from_user.id, within)

	texts = f"<b>List of expenses and income for {'the last day' if within == 'day' else 'all time' if within == '*' else 'the last month'}</b>\n\n"
	for transaction in transactions:
		texts += f"{'Earned by' if transaction.profit else 'Spent'} <b>{transaction.amount}$</b> on {transaction.date}\n"
	
	return await message.reply(texts)