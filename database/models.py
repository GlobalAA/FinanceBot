from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field


class UserModel(BaseModel):
	id: Optional[int] = Field(None, description="User id (Auto increment)")
	user_id: int = Field(..., description="Telegram user id")
	fullname: str = Field(..., description="Fullname of user")
	join_date: datetime = Field(..., description="Join date (UNIX timestamp)")
	
class TransactionModel(BaseModel):
	id: Optional[int] = Field(None, description="Transaction id (Auto increment)")
	user_id: int = Field(..., description="Telegram user id")
	amount: int = Field(..., description="Amount of transaction")
	profit: bool = Field(False, description="Profit or not")
	date: datetime = Field(..., description="Date of transaction (UNIX timestamp)")