from enum import Enum

from aiogram.filters.callback_data import CallbackData


class ActionType(str, Enum):
	next = "NEXT"
	back = "BACK"

class WithinType(str, Enum):
	month = "month"
	day = "day"
	all = "*"

class ActionData(CallbackData, prefix="my"):
	id: int
	within: WithinType
	action: ActionType