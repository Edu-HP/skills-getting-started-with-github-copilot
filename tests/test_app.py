import pytest
from fastapi.testclient import TestClient
from src.app import app, activities

client = TestClient(app)

# Utilidad para limpiar participantes antes de cada test
def reset_participants():
    for act in activities.values():
        act['participants'] = act['participants'][:2]  # restaurar a los dos iniciales

@pytest.fixture(autouse=True)
def run_before_tests():
    reset_participants()


def test_get_activities():
    response = client.get("/activities")
    assert response.status_code == 200
    data = response.json()
    assert "Chess Club" in data
    assert "participants" in data["Chess Club"]


def test_signup_for_activity():
    email = "nuevo@mergington.edu"
    response = client.post(f"/activities/Chess Club/signup?email={email}")
    assert response.status_code == 200
    assert email in activities["Chess Club"]["participants"]


def test_signup_duplicate():
    email = activities["Chess Club"]["participants"][0]
    response = client.post(f"/activities/Chess Club/signup?email={email}")
    assert response.status_code == 400
    assert response.json()["detail"] == "Student already signed up for this activity"


def test_signup_activity_not_found():
    response = client.post("/activities/NoExiste/signup?email=alguien@mergington.edu")
    assert response.status_code == 404


def test_unregister_from_activity():
    email = activities["Chess Club"]["participants"][0]
    response = client.delete(f"/activities/Chess Club/unregister?email={email}")
    assert response.status_code == 200
    assert email not in activities["Chess Club"]["participants"]


def test_unregister_not_registered():
    email = "noexiste@mergington.edu"
    response = client.delete(f"/activities/Chess Club/unregister?email={email}")
    assert response.status_code == 400
    assert response.json()["detail"] == "Student not registered for this activity"


def test_unregister_activity_not_found():
    response = client.delete("/activities/NoExiste/unregister?email=alguien@mergington.edu")
    assert response.status_code == 404
