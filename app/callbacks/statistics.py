import asyncio
import os

import pandas as pd
from aiogram import F, Router
from aiogram.types import CallbackQuery, FSInputFile
from aiogram.utils.chat_action import ChatActionSender
from babel.dates import format_datetime

from app.models.models import Transaction, User

router = Router()

@router.callback_query(F.data.startswith("get_"))
async def get_statistic_file(call: CallbackQuery):
	id = call.data.split("_")[-1]
	user = await User.get_or_none(user_id=id)


	if not user:
		return await call.answer("Сталася помилка, повідомте адміністратора")

	transactions = await Transaction.filter(user_id=id)

	async with ChatActionSender.upload_document(bot=call.bot, chat_id=call.message.chat.id):
		await asyncio.sleep(1)
		data = [
			{
				"Id": t.id,
				"Сума": format(t.amount, "f"),
				"Тип": 'Дохід' if t.profit else 'Витрата',
				"Додана": format_datetime(t.date, "EEEE, d MMMM y", locale="uk").capitalize()
			}
			for t in transactions
		]

		filepath = f"report_{id}.xlsx"
		df = pd.DataFrame(data)
		df.to_excel(filepath, index=False)
		
		if os.path.exists(filepath):
			file = FSInputFile(filepath)
			await call.message.answer_document(document=file, caption=f"Фінансовий звіт користувача {call.from_user.full_name}")
			return os.remove(filepath)
		else:
			return await call.answer("Сталася помилка, повідомте адміністратора")

