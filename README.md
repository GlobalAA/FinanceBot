## Фінансовий бот (Finance bot)

The bot has a simple functionality, you will be able to add income and expenses, so-called transactions, and get them

| Commands |                                 Arguments                                  | Description                    |
| :------: | :------------------------------------------------------------------------: | ------------------------------ |
|   earn   |                                   amount                                   | Add earn transaction           |
|  spend   |                                   amount                                   | Add spend transaction          |
|   all    | day<br />month<br />no argument<br />(selects all transactions by default) | Get all transactions by filter |

Stack:

- aiogram
- sqlite3
- pydantic and pydantic_settings
