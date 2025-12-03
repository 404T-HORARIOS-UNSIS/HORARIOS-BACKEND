from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_list_exams_empty():
    r = client.get("/examenes/exams")
    assert r.status_code == 200
    assert isinstance(r.json(), list)


def test_seed_pdf_data_then_list():
    r = client.post("/examenes/seed-pdf-data")
    assert r.status_code == 200
    msg = r.json().get("message", "")
    assert "cargados" in msg.lower() or "cargados previamente" in msg.lower()

    r = client.get("/examenes/exams")
    assert r.status_code == 200
    data = r.json()
    assert isinstance(data, list)
    assert len(data) >= 1
    item = data[0]
    for key in ["id", "course", "group", "professor", "classroom", "date", "start", "end"]:
        assert key in item
