from bs.models import Article
import uuid


def test_read_articles(session, client):
    a = Article(body="1", title="1")
    b = Article(body="2", title="2")
    session.add(a)
    session.add(b)
    
    resp = client.get("/articles/")
    assert resp.status_code == 200
    assert len(resp.json()) == 2


def test_post_article(session, client):   
    resp = client.post("/articles/", json={"body": "body", "title": "title"})
    assert resp.status_code == 200
    data = resp.json()
    id_ = data.get("id")

    resp = client.get(f"articles/{id_}")
    assert resp.status_code == 200

    new_article = session.get(Article, uuid.UUID(id_))
    assert new_article.body == "body"
    assert new_article.title == "title"


def test_get_article_by_key(session, client):
    id_ = uuid.uuid4()
    body = "body1"
    title = "title1"

    a = Article(id=id_, body=body, title=title)
    session.add(a)

    resp = client.get(f"/articles/{id_}")
    assert resp.status_code == 200
    data = resp.json()
    assert data["body"] == body
    assert data["title"] == title
    assert data["id"] == str(id_)

def test_update_article(client, session):
    a = Article(body="1", title="1")
    b = Article(body="2", title="2")
    session.add(a)
    session.add(b)

    id_ = a.id

    resp = client.patch(f"articles/{str(id_)}", params={"title": "3", "body":"4"})
    assert resp.status_code == 200

    session.refresh(a)
    assert a.title == "3"
    assert a.body == "4"


def test_delete_article(client, session):
    a = Article(body="1", title="1")
    b = Article(body="2", title="2")
    session.add(a)
    session.add(b)
    
    id_ = a.id

    client.delete(f"articles/{id_}")

    assert session.get(Article, id_) is None
