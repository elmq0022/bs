from fastapi import FastAPI, HTTPException, Query
from bs.models import Article
import uuid

from typing import Annotated

from sqlalchemy import select
from fastapi import Depends


from sqlmodel import (
    Session,
    create_engine,
)


sqlite_file_name = "db.sqlite3"
sqlite_url = f"sqlite:///{sqlite_file_name}"

connect_args = {"check_same_thread": False}
engine = create_engine(sqlite_url, connect_args=connect_args)


def get_session():
    with Session(engine) as session:
        yield session


SessionDep = Annotated[Session, Depends(get_session)]


app = FastAPI()


@app.post("/articles/")
def create_article(article: Article, session: SessionDep) -> Article:
    session.add(article)
    session.commit()
    session.refresh(article)
    return article


@app.get("/articles/")
def read_articles(
    session: SessionDep, offset: int = 0, limit: Annotated[int, Query(le=100)] = 100
) -> list[Article]:
    statement = select(Article)
    statement = statement.offset(offset)
    statement = statement.limit(limit)
    articles = session.exec(statement).scalars().all()
    return articles


@app.patch("/articles/{article_id}")
def update_article(
    session: SessionDep,
    article_id: uuid.UUID,
    title: str|None = None,
    body: str|None = None,
) -> Article:
    article = session.get(Article, article_id)

    if not article:
        raise HTTPException(status_code=404, detail="Article not found")

    if title:
        article.title = title

    if body:
        article.body = body

    session.commit()
    session.refresh(article)
    return article


@app.get("/articles/{article_id}")
def read_article(article_id: uuid.UUID, session: SessionDep) -> Article:
    article = session.get(Article, article_id)
    if not article:
        raise HTTPException(status_code=404, detail="Article not found")
    return article


@app.delete("/articles/{article_id}")
def delete_article(article_id: uuid.UUID, session: SessionDep):
    article = session.get(Article, article_id)
    if not article:
        raise HTTPException(status_code=404, detail="Article not found")
    session.delete(article)
    session.commit()
    return {"ok": True}
