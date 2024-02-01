from fastapi.testclient import TestClient
from sqlalchemy import create_engine, StaticPool
from sqlalchemy.orm import sessionmaker

from database import Base
from main import app, get_db

SQLALCHEMY_DATABASE_URL = "sqlite:///:memory:"
engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False},
    poolclass=StaticPool
)
test_session = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base.metadata.create_all(bind=engine)


def override_get_db():
    db = test_session()
    try:
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db] = override_get_db
client = TestClient(app)


def test_read_empty_todo():
    response = client.get("/todo")
    assert response.status_code == 200
    assert response.json() == []


def test_post_todo():
    response = client.post("/todo", data={"description": "string",
                                          "due-date": "2024-02-01T05:29:14"
                                                      ".467Z",
                                          "done": False, "priority": 0})
    # assert response.status_code == 201
    assert response.json() == {"id": 1, "description": "string",
                               "due-date": "2024-02-01T05:29:14.467000",
                               "done": False, "priority": 0}


def test_get_todo_by_id():
    response = client.get("/todo/1")
    assert response.status_code == 200
    assert response.json() == {"id": 1, "description": "string",
                               "due-date": "2024-02-01T05:29:14.467000",
                               "done": False, "priority": 0}


def test_get_todo_by_invalid_id():
    response = client.get("/todo/9999")
    assert response.status_code == 404
    assert response.json() == {"detail": "Todo with id 9999 not found"}


def test_update_todo():
    response = client.patch("/todo/1")
    assert response.status_code == 204

    response = client.get("/todo/1")
    assert response.status_code == 200
    assert response.json() == {"id": 1, "description": "string",
                               "due-date": "2024-02-01T05:29:14.467000",
                               "done": True, "priority": 0}


def test_update_non_existent_todo():
    response = client.patch("/todo/999")
    assert response.status_code == 404


def test_delete_todo():
    response = client.delete("/todo/1")
    assert response.status_code == 204


def test_delete_todo_by_invalid_id():
    response = client.delete("/todo/9999")
    assert response.status_code == 404
