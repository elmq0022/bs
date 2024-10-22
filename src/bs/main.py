import uuid
from typing import Annotated

from fastapi import Depends, FastAPI, HTTPException, Query
from sqlalchemy import select
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.orm import sessionmaker
from sqlmodel import SQLModel
from sqlmodel.ext.asyncio.session import AsyncSession

from bs.models import Article

sqlite_file_name = "db.sqlite3"
sqlite_url = f"sqlite+aiosqlite:///{sqlite_file_name}"

connect_args = {"check_same_thread": False}
engine = create_async_engine(sqlite_url, connect_args=connect_args)


async def get_session() -> AsyncSession:
    async_session = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)
    async with async_session() as session:
        yield session


SessionDep = Annotated[AsyncSession, Depends(get_session)]


app = FastAPI()


@app.post("/articles/")
async def create_article(article: Article, session: SessionDep) -> Article:
    session.add(article)
    await session.commit()
    await session.refresh(article)
    return article


@app.get("/articles/")
async def read_articles(
    session: SessionDep, offset: int = 0, limit: Annotated[int, Query(le=100)] = 100
) -> list[Article]:
    statement = select(Article)
    statement = statement.offset(offset)
    statement = statement.limit(limit)
    articles = await session.exec(statement)
    articles = articles.scalars().all()
    return articles


@app.patch("/articles/{article_id}")
async def update_article(
    session: SessionDep,
    article_id: uuid.UUID,
    title: str | None = None,
    body: str | None = None,
) -> Article:
    article = await session.get(Article, article_id)

    if not article:
        raise HTTPException(status_code=404, detail="Article not found")

    if title:
        article.title = title

    if body:
        article.body = body

    await session.commit()
    await session.refresh(article)
    return article


@app.get("/articles/{article_id}")
async def read_article(article_id: uuid.UUID, session: SessionDep) -> Article:
    article = await session.get(Article, article_id)
    if not article:
        raise HTTPException(status_code=404, detail="Article not found")
    return article


@app.delete("/articles/{article_id}")
async def delete_article(article_id: uuid.UUID, session: SessionDep):
    article = await session.get(Article, article_id)
    if not article:
        raise HTTPException(status_code=404, detail="Article not found")

    await session.delete(article)
    await session.commit()
    return {"ok": True}
