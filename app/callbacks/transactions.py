from typing import List

from aiogram import F, Router
from aiogram.types import CallbackQuery
from aiogram.utils.keyboard import InlineKeyboardBuilder

from app.models.models import Transaction
from app.utils import get_transactions

from .types import ActionData, ActionType, WithinType

router = Router()

def build_navigation_keyboard(current_page: int, within: WithinType) -> InlineKeyboardBuilder:
	builder = InlineKeyboardBuilder()
	builder.button(
		text="⬅️ Назад",
		callback_data=ActionData(id=current_page - 1, action=ActionType.back, within=within).pack()
	)
	builder.button(
		text="➡️ Далі",
		callback_data=ActionData(id=current_page + 1, action=ActionType.next, within=within).pack()
	)
	builder.adjust(2)
	return builder

def build_transactions_text(transactions: List[Transaction], within: WithinType) -> str:
	header_map = {
		"day": "останній день",
		"*": "весь час",
		"month": "останній місяць"
	}
	header = header_map.get(within, "період")
	lines = [f"<b>Список доходів і витрат за {header}</b>\n"]

	for t in transactions:
		sign = "➕" if t.profit else "➖"
		formatted = t.date.strftime("%A, %d %B %Y")
		lines.append(f"{sign} <b>{t.amount}</b> грн ({formatted})")

	return "\n".join(lines)

async def edit_message(
    call: CallbackQuery,
    transactions: List[Transaction],
    page: int,
    within: WithinType
):
	text = build_transactions_text(transactions, within)
	keyboard = build_navigation_keyboard(page, within)
	await call.message.edit_text(text=text, reply_markup=keyboard.as_markup())



@router.callback_query(ActionData.filter(F.action.in_([ActionType.back, ActionType.next])))
async def navigate(call: CallbackQuery, callback_data: ActionData):
	transactions = await get_transactions(call.from_user.id, callback_data.within)

	if not transactions:
		return await call.answer("Немає жодних даних")

	page = callback_data.id
	start = page * 10
	end = start + 10

	if start >= len(transactions) or start < 0:
		return await call.answer("Більше даних не знайдено")

	current_transactions = transactions[start:end]
	await edit_message(call, current_transactions, page, callback_data.within)