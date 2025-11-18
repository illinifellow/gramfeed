import asyncio

from alembic import context
from sqlalchemy.ext.asyncio import create_async_engine

from gramfeed.db.models import Base
from gramfeed.settings import settings


def run(connection):
    context.configure(connection=connection, target_metadata=Base.metadata)
    with context.begin_transaction():
        context.run_migrations()


async def main():
    engine = create_async_engine(settings().database_url)
    async with engine.connect() as conn:
        await conn.run_sync(run)