from tortoise import BaseDBAsyncClient


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE "transaction" ALTER COLUMN "amount" TYPE DECIMAL(10,2) USING "amount"::DECIMAL(10,2);
        ALTER TABLE "transaction" ALTER COLUMN "amount" TYPE DECIMAL(10,2) USING "amount"::DECIMAL(10,2);"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE "transaction" ALTER COLUMN "amount" TYPE INT USING "amount"::INT;"""
