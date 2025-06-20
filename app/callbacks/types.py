from enum import Enum

from aiogram.filters.callback_data import CallbackData


class ActionType(str, Enum):
	next = "NEXT"
	back = "BACK"

class WithinType(str, Enum):
	all_time = "*"
	day = "day"
	month = "month"

class ActionData(CallbackData, prefix="finance"):
	id: int
	within: WithinType
	action: ActionType