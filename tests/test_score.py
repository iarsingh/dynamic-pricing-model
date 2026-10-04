from fastapi.testclient import TestClient
from pricing.main import app

client = TestClient(app)


def test_high_and_low():
    assert client.post("/score", json={'demand': 40, 'inventory': 2, 'cost': 20}).json()["label"]
    high = client.post("/score", json={'demand': 40, 'inventory': 2, 'cost': 20}).json()
    low = client.post("/score", json={'demand': 5, 'inventory': 80, 'cost': 8}).json()
    assert high["label"] != low["label"]
    assert high["score"] > low["score"]


def test_missing_is_refused():
    body = dict({'demand': 40, 'inventory': 2, 'cost': 20})
    body.pop("demand")
    assert client.post("/score", json=body).status_code == 422
