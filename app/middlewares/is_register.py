from typing import Any, Awaitable, Callable, Dict

from aiogram import BaseMiddleware
from aiogram.types import Message
from aiogram.types import User as TUser

from app.models.models import User


class RegisterMiddleware(BaseMiddleware):
	async def __call__(
		self,
		handler: Callable[[Message, Dict[str, Any]], Awaitable[Any]],
		event: Message,
		data: Dict[str, Any]
	) -> Any:
		t_user: TUser = data["event_from_user"]
		id: int = t_user.id

		await User.get_or_create(user_id=id)

		return await handler(event, data)