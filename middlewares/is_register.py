from typing import Any, Awaitable, Callable, Dict

from aiogram import BaseMiddleware
from aiogram.types import TelegramObject, User

from constants import db


class RegisterMiddleware(BaseMiddleware):
	async def __call__(
		self,
		handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
		event: TelegramObject,
		data: Dict[str, Any]
	) -> Any:
		user: User = data["event_from_user"]
		fullname = f"{user.first_name} {user.last_name}" if not user.username else user.username
		
		if not db.get_user(user.id):
			db.add_user(user.id, fullname)

		return await handler(event, data)