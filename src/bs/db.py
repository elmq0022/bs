from typing import Annotated

from fastapi import Depends
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.orm import sessionmaker
from sqlmodel.ext.asyncio.session import AsyncSession
from pathlib import Path
from alembic import command, config


parent = Path(__file__).parent
sqlite_file_name = parent / "db.sqlite3"
sqlite_file_name = str(sqlite_file_name.absolute())
sqlite_url = f"sqlite+aiosqlite:///{sqlite_file_name}"

alembic_ini = parent / "alembic.ini"
alembic_script = parent / "migrations"

connect_args = {"check_same_thread": False}
engine = create_async_engine(sqlite_url, connect_args=connect_args)


def run_upgrade(connection, cfg):
    cfg.attributes["connection"] = connection
    command.upgrade(cfg, "head")


async def run_async_upgrade():
    cfg = config.Config(str(alembic_ini.absolute()))
    cfg.set_main_option("script_location", "bs:migrations")
    async with engine.begin() as conn:
        await conn.run_sync(run_upgrade, cfg)


async def get_session():
    async_session = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)
    async with async_session() as session:
        yield session


SessionDep = Annotated[AsyncSession, Depends(get_session)]
