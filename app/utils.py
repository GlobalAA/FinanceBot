from datetime import datetime, timedelta

from app.models.models import Transaction


async def get_transactions(user_id: int, within: str = "day"):
	now = datetime.now()

	if within == "day":
		start_date = now.replace(hour=0, minute=0, second=0, microsecond=0)
	if within == "month":
		start_date = now - timedelta(days=30)

	if within != "*":
		transactions = await Transaction.filter(user_id=user_id, date__gte=start_date).order_by('date')	
	else:
		transactions = await Transaction.filter(user_id=user_id).order_by('date')	
	
	return transactions