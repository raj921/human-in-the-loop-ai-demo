import os
import tempfile

import pytest
from fastapi.testclient import TestClient

from src.backend.api import app
from src.backend import config


@pytest.fixture(autouse=True)
def _temp_db_env(monkeypatch):
    with tempfile.TemporaryDirectory() as tmp:
        db_url = f"sqlite:///{os.path.join(tmp, 'test.db')}"
        monkeypatch.setenv("FD_DATABASE_URL", db_url)
        # Recreate settings so it picks up env changes
        config.settings = config.Settings()  # type: ignore
        yield


def test_create_request_known_answer(monkeypatch):
    client = TestClient(app)

    # Preload knowledge by responding to a fake request path
    r = client.post("/requests", json={"caller_id": "c1", "question": "hours"})
    assert r.status_code == 200
    data = r.json()
    assert data["known"] is False
    req_id = data["request_id"]

    r = client.post(f"/requests/{req_id}/respond", json={"answer": "9-5 daily"})
    assert r.status_code == 200

    # Now the same question should be known
    r = client.post("/requests", json={"caller_id": "c2", "question": "hours"})
    assert r.status_code == 200
    data = r.json()
    assert data["known"] is True
    assert data["answer"] == "9-5 daily"


def test_list_and_timeout_flow():
    client = TestClient(app)

    r = client.post("/requests", json={"caller_id": "c3", "question": "price"})
    assert r.status_code == 200
    req_id = r.json()["request_id"]

    r = client.get("/requests")
    assert r.status_code == 200
    assert any(item["id"] == req_id for item in r.json())

    r = client.post("/timeouts/sweep")
    assert r.status_code == 200
    assert "unresolved" in r.json()


