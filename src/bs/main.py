import uuid
from typing import Annotated

from fastapi import FastAPI, HTTPException, Query
from sqlalchemy import select

from bs.db import SessionDep
from bs.models import Article

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
