from typing import List

from aiogram import F, Router
from aiogram.types import CallbackQuery
from aiogram.utils.keyboard import InlineKeyboardBuilder

from constants import db
from database import TransactionModel

from .models import ActionData, ActionType, WithinType

router = Router(name="callbacks_router")

async def edit_message(id: int, data: List[TransactionModel], call_data: CallbackQuery, within: WithinType):
	texts = f"<b>Список доходів і витрат за {'останній день' if within == 'day' else 'весь час' if within == '*' else 'останній місяць'}</b>\n\n"

	builder = InlineKeyboardBuilder()
	builder.button(
		text="Назад" ,
		callback_data=ActionData(id=id, action=ActionType.back, within=within).pack()
	)
	builder.button(
		text="Далі" ,
		callback_data=ActionData(id=id, action=ActionType.next, within=within).pack()
	)
	builder.adjust(2)

	for transaction in data:
		texts += f"{'➕' if transaction.profit else '➖'} <b>{transaction.amount}</b>грн ({transaction.date})\n"

	await call_data.message.edit_text(text=texts, reply_markup=builder.as_markup())

@router.callback_query(ActionData.filter(F.action == ActionType.back))
@router.callback_query(ActionData.filter(F.action == ActionType.next))
async def finance_navigate(call: CallbackQuery, callback_data: ActionData):
	transactions = db.get_transactions(call.from_user.id, callback_data.within)
	id = callback_data.id * 10

	if transactions is None:
		return await call.answer("Немає жодних даних")

	if callback_data.action == ActionType.next:
		id += 10
	elif callback_data.action == ActionType.back:
		id -= 10 if id > 0 else 0

	if abs(id) >= len(transactions) or id == callback_data.id * 10:
		return await call.answer("Більше даних не знайдено")

	data = transactions[:10] if id == 0 else transactions[id:id+10]

	await edit_message(id / 10, data, call, callback_data.within)