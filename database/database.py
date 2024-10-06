import sqlite3
from typing import List

from .models import TransactionModel, UserModel


class BotDB:
	def __init__(self):
		self.conn = sqlite3.connect("bot.db")
		self.cursor = self.conn.cursor()

		self.cursor.execute("""
		CREATE TABLE IF NOT EXISTS users (
			id INTEGER PRIMARY KEY AUTOINCREMENT,
			user_id INTEGER NOT NULL UNIQUE,
			fullname TEXT NOT NULL,
			join_date DATETIME DEFAULT CURRENT_TIMESTAMP		
		)
		""")

		self.cursor.execute("""
		CREATE TABLE IF NOT EXISTS transactions (
			id INTEGER PRIMARY KEY AUTOINCREMENT,
			user_id INTEGER NOT NULL,
			amount INTEGER NOT NULL,
			profit BOOLEAN NOT NULL DEFAULT False,
			date DATETIME DEFAULT CURRENT_TIMESTAMP,
			FOREIGN KEY (user_id) REFERENCES users (user_id)
		)
		""")

		self.conn.commit()

	def get_user(self, user_id) -> UserModel:
		self.cursor.execute("SELECT * FROM users WHERE user_id = ?", (user_id,))
		row = self.cursor.fetchone()

		if row:
			return UserModel(
				id=row[0],
				user_id=row[1],
				fullname=row[2],
				join_date=row[3]
			)

		return None
	
	def add_user(self, user_id, fullname) -> bool:
		try:
			self.cursor.execute("INSERT INTO users (user_id, fullname) VALUES (?, ?)", (user_id, fullname))
			self.conn.commit()
			return True
		except:
			return False
		
	def get_transactions(self, user_id, within = "*") -> List[TransactionModel] | None:
		if within == "day":
			self.cursor.execute("SELECT * FROM transactions WHERE user_id = ? AND date BETWEEN datetime('now', 'start of day') AND datetime('now', 'localtime') ORDER BY date", (user_id,))
			row = self.cursor.fetchall()

		elif within == "month":
			self.cursor.execute("SELECT * FROM transactions WHERE user_id = ? AND date BETWEEN datetime('now', '-1 month') AND datetime('now', 'localtime') ORDER BY date", (user_id, ))
			row = self.cursor.fetchall()

		elif within == "*":
			self.cursor.execute("SELECT * FROM transactions WHERE user_id = ? ORDER BY date", (user_id,))
			row = self.cursor.fetchall()
		
		if row:
			return [TransactionModel(
				id=r[0],
				user_id=r[1],
				amount=r[2],
				profit=r[3],
				date=r[4]
			) for r in row]

		return None
	
	def add_transaction(self, user_id, amount, profit):
		self.cursor.execute("INSERT INTO transactions (user_id, amount, profit) VALUES (?, ?, ?)", (user_id, amount, profit))
		self.conn.commit()

	def __del__(self):
		self.cursor.close()
		self.conn.close()