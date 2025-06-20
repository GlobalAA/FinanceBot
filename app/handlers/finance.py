import re
from decimal import Decimal

from aiogram import Router
from aiogram.filters import Command, CommandObject, CommandStart
from aiogram.types import Message
from aiogram.utils.keyboard import InlineKeyboardBuilder
from babel.dates import format_datetime
from tortoise.exceptions import IntegrityError
from tortoise.functions import Sum

from app.callbacks.types import ActionData, ActionType, WithinType
from app.middlewares import RegisterMiddleware
from app.models.models import Transaction, User
from app.utils import get_transactions

router = Router()
router.message.middleware(RegisterMiddleware())

def is_decimal_regex(s):
	pattern = r"^[+-]?\d+(\.\d+)?$"
	return re.match(pattern, s) is not None

def build_keyboard(within: WithinType):
	builder = InlineKeyboardBuilder()
	builder.button(
		text="Назад",
		callback_data=ActionData(id=1, action=ActionType.back, within=within).pack()
	)
	builder.button(
		text="Далі",
		callback_data=ActionData(id=1, action=ActionType.next, within=within).pack()
	)
	builder.adjust(2)

	return builder

@router.message(CommandStart())
async def start_cmd(message: Message):
	text = '''Вітаю! Я ваш персональний асистент для фінансового обліку (основна валюта — гривня). 💼
Я допоможу вам ефективно відстежувати доходи та витрати.

Доступні команди:
/spend — додати витрати
/earn — додати дохід
/all — переглянути всі записи по доходах і витратах'''
	return await message.answer(text)

@router.message(Command(commands=["spend", "earn"]))
async def spend_earn_command(message: Message, command: CommandObject):
	arg = command.args.split(" ")[0] if command.args else None

	if arg == None or not is_decimal_regex(arg):
		return await message.answer("Введіть будь-ласка число. (100 або 100.0)")
	
	amount: Decimal = Decimal(command.args.split(" ")[0])

	user: User = await User.get_or_none(user_id=message.from_user.id)

	if not user:
		return await message.answer("Ви не зареєстровані. Сталася помилка, будь-ласка повідомте адміністратора")
	
	try:
		await Transaction.create(
			user=user,
			amount=amount,
			profit=command.command == "earn"
		)
	except IntegrityError:
		return await message.answer("Сталася помилка, будь-ласка повідомте адміністратора")
	
	return await message.reply(f"Додано {amount} до ваших {'доходів' if command.command == 'earn' else 'витрат'}")

@router.message(Command("all"))
async def all_values(message: Message, command: CommandObject):
	user = await User.get_or_none(user_id=message.from_user.id)
	if not user:
		return await message.reply("Ви не зареєстровані. Сталася помилка, будь-ласка повідомте адміністратора")


	within = WithinType.all_time
	if command.args:
		arg = command.args.split(" ")[0].lower()
		try:
			within = WithinType(arg if arg != "*" else WithinType.all_time)
		except ValueError:
			return await message.reply("Некоректно викликана команда. Використовуйте /all <day/month>")

	transactions = await get_transactions(user.user_id, within.value)

	header_map = {
		WithinType.day: "останній день",
		WithinType.month: "останній місяць",
		WithinType.all_time: "весь час"
	}
	text = f"<b>Список доходів і витрат за {header_map.get(within)}</b>\n\n"

	for transaction in transactions[:10]:
		sign = "➕" if transaction.profit else "➖"
		formatted = transaction.date.strftime("%A, %d %B %Y")
		text += f"{sign} <b>{transaction.amount}</b> грн ({formatted})\n"

	builder = build_keyboard(within)

	return await message.reply(text, reply_markup=builder.as_markup())

@router.message(Command(commands=["stat", "statistic"]))
async def statistic(message: Message):
	user = await User.get_or_none(user_id=message.from_user.id)
	if not user:
		return await message.reply("Ви не зареєстровані. Сталася помилка, будь-ласка повідомте адміністратора")
	
	spend_sum_f = await Transaction.filter(user_id=user.user_id, profit=False).annotate(total_sum=Sum("amount")).values("total_sum")
	earn_sum_f = await Transaction.filter(user_id=user.user_id, profit=True).annotate(total_sum=Sum("amount")).values("total_sum")

	spend_sum = spend_sum_f[0]["total_sum"] if spend_sum_f else 0
	earn_sum = earn_sum_f[0]["total_sum"] if earn_sum_f else 0

	coefficient = spend_sum/earn_sum
	coefficient_text = ""

	if coefficient < 1:
		coefficient_text = "Нормальний (витрати менші за доходи)"
	elif coefficient_text == 1:
		coefficient_text = "Нульовий (витрати = доходи)"
	else:
		coefficient_text = "Надлишковий (витрати більші за доходи)"

	join_date = format_datetime(user.join_date, "EEEE, d MMMM y", locale="uk").capitalize()

	text = f'''📊 Статистика за період починаючи з {user.join_date.strftime('%d.%m.%Y')}
	
👤 Ім'я: {message.from_user.full_name}
🗓 Дата реєстрації: {join_date}

🧾 Коефіцієнт: {coefficient_text}
⬇️ Усього витрачено: {format(spend_sum, 'f')}грн
⬆️ Усього отримано: {format(earn_sum, 'f')}грн'''
	
	builder = InlineKeyboardBuilder()
	builder.button(text="Завантажити звіт", callback_data=f"get_{user.user_id}")
	builder.adjust(1)
	
	return await message.answer(text, reply_markup=builder.as_markup())