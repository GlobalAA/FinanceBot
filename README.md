# Financial Bot

A simple Telegram bot for tracking your income and expenses. Built with Python, Aiogram, and Tortoise ORM, this bot lets you record transactions, view summaries, and generate reports — all within your favorite messaging app.

## Features

- **Add Expenses & Income**
  - `/spend <amount>` — Record a new expense.
  - `/earn <amount> `— Record new income.
- **View All Records**
  - `/all <day/month>` — List all transactions (can be filtered by day or month, as desired).
- **Statistics & Reports**
  - `/stat` or `/statistic` — Show summary statistics.
  - Inline button to download a full report.
- **Start & Help**
  - `/start` — Welcome message and basic instructions

---

## Installation

1. **Clone the repository**

   ```bash
   git clone https://github.com/yourusername/finance-bot.git
   cd finance-bot
   ```

2. **Install dependencies** Using [Poetry](https://python-poetry.org/):

   ```bash
   poetry install
   ```

3. **Configure environment variables**
   Create a `.env` file in the project root:

   ```env
   BOT_TOKEN=<your-telegram-bot-token>
   DATABASE_URL=postgres://user:password@host:port/database
   ```

   – `BOT_TOKEN`: obtained from [@BotFather](https://t.me/BotFather).
   – `DATABASE_URL`: your PostgreSQL connection string.

---

## Database Migrations

Before running the bot, make sure your database schema is up to date:

```bash
# Initialize Aerich (only once)
aerich init-db

# Generate a new migration after model changes
aerich migrate --name <migration_name>

# Apply migrations
aerich upgrade
```

---

## Running the Bot

Once everything is set up:

```bash
poetry run python -m app
```

Or directly:

```bash
python -m app
```

You should see log output indicating the bot has started. Send `/start` to your bot in Telegram to begin.

---

## Project Structure

```
.
├── app/
│   ├── __main__.py         # Entry point
│   ├── config.py           # Settings and environment loading
│   ├── handlers/           # Command and callback handlers
│   ├── models/             # Tortoise ORM models
│   ├── middlewares/        # Aiogram middlewares
│   ├── utils.py            # Helper functions
│   └── tortoise_config.py  # ORM configuration
├── migrations/             # Aerich migrations
├── pyproject.toml          # Poetry config
└── README.md               # This file
```
