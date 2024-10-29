import uuid

import pytest

from bs.models import Article

pytestmark = pytest.mark.anyio


async def test_read_articles(session, client):
    a = Article(body="1", title="1")
    b = Article(body="2", title="2")
    session.add(a)
    session.add(b)

    resp = client.get("/v1/articles/")
    assert resp.status_code == 200
    assert len(resp.json()) == 2


async def test_post_article(session, client):
    resp = client.post("/v1/articles/", json={"body": "body", "title": "title"})
    assert resp.status_code == 200
    data = resp.json()
    id_ = data.get("id")

    resp = client.get(f"/v1/articles/{id_}")
    assert resp.status_code == 200

    new_article = await session.get(Article, uuid.UUID(id_))
    assert new_article.body == "body"
    assert new_article.title == "title"


async def test_get_article_by_key(session, client):
    id_ = uuid.uuid4()
    body = "body1"
    title = "title1"

    a = Article(id=id_, body=body, title=title)
    session.add(a)

    resp = client.get(f"/v1/articles/{id_}")
    assert resp.status_code == 200
    data = resp.json()
    assert data["body"] == body
    assert data["title"] == title
    assert data["id"] == str(id_)


async def test_update_article(client, session):
    a = Article(body="1", title="1")
    b = Article(body="2", title="2")
    session.add(a)
    session.add(b)

    id_ = a.id

    resp = client.patch(f"/v1/articles/{str(id_)}", params={"title": "3", "body": "4"})
    assert resp.status_code == 200

    await session.refresh(a)
    assert a.title == "3"
    assert a.body == "4"


async def test_delete_article(client, session):
    a = Article(body="1", title="1")
    b = Article(body="2", title="2")
    session.add(a)
    session.add(b)

    id_ = a.id

    resp = client.delete(f"/v1/articles/{id_}")

    assert resp.status_code == 200
    assert resp.json() == {"ok": True}
    assert await session.get(Article, id_) is None
