from tortoise import Model, fields


class User(Model):
	id = fields.IntField(pk=True)
	user_id = fields.IntField(unique=True)
	join_date = fields.DatetimeField(auto_now_add=True)

	transactions: fields.ReverseRelation["Transaction"]

class Transaction(Model):
	id = fields.IntField(pk=True)
	user: fields.ForeignKeyRelation[User] = fields.ForeignKeyField(
		"models.User", related_name="transactions", to_field="user_id"
	)
	amount = fields.DecimalField(max_digits=10, decimal_places=2)
	profit = fields.BooleanField(default=False)
	date = fields.DatetimeField(auto_now_add=True)
