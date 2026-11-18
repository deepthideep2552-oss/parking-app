import pytest
import app as parking


@pytest.fixture
def client():
    parking.app.config["TESTING"] = True
    parking.slots = parking.create_slots()          # fresh parking lot for every test
    return parking.app.test_client()


def test_home_page_loads(client):
    res = client.get("/")
    assert res.status_code == 200
    assert b"Parking Slot Booking System" in res.data


def test_health_check(client):
    assert client.get("/health").get_json()["status"] == "UP"


def test_all_slots_free_at_start(client):
    data = client.get("/api/slots").get_json()
    assert data["summary"] == {"total": 16, "booked": 0, "free": 16}


def test_book_slot(client):
    client.post("/book", data={"slot_id": "A1", "vehicle": "TN01AB1234", "owner": "Ravi"})
    data = client.get("/api/slots").get_json()
    a1 = next(s for s in data["slots"] if s["id"] == "A1")
    assert a1["booked"] and a1["vehicle"] == "TN01AB1234"
    assert data["summary"]["booked"] == 1


def test_cannot_double_book(client):
    client.post("/book", data={"slot_id": "A1", "vehicle": "TN01AB1234"})
    client.post("/book", data={"slot_id": "A1", "vehicle": "KA05XY9999"})
    a1 = next(s for s in client.get("/api/slots").get_json()["slots"] if s["id"] == "A1")
    assert a1["vehicle"] == "TN01AB1234"


def test_release_slot(client):
    client.post("/book", data={"slot_id": "B2", "vehicle": "TN09CD5678"})
    client.post("/release/B2")
    assert client.get("/api/slots").get_json()["summary"]["booked"] == 0
