import pytest
from fastapi.testclient import TestClient
from src.app import app, activities

client = TestClient(app)

def test_root_redirect():
    response = client.get("/")
    assert response.status_code == 200 or response.status_code == 307
    # Should redirect to /static/index.html
    assert str(response.url).endswith("/static/index.html")

def test_get_activities():
    response = client.get("/activities")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, dict)
    assert "Chess Club" in data
    assert "Programming Class" in data

def test_signup_success():
    activity = "Chess Club"
    email = "testuser@mergington.edu"
    # Ensure user is not already signed up
    if email in activities[activity]["participants"]:
        activities[activity]["participants"].remove(email)
    response = client.post(f"/activities/{activity}/signup", params={"email": email})
    assert response.status_code == 200
    assert f"Signed up {email} for {activity}" in response.json()["message"]
    assert email in activities[activity]["participants"]

def test_signup_already_signed_up():
    activity = "Chess Club"
    email = "testuser@mergington.edu"
    # Ensure user is signed up
    if email not in activities[activity]["participants"]:
        activities[activity]["participants"].append(email)
    response = client.post(f"/activities/{activity}/signup", params={"email": email})
    assert response.status_code == 400
    assert response.json()["detail"] == "Already signed up for this activity"

def test_signup_activity_not_found():
    response = client.post("/activities/Nonexistent/signup", params={"email": "someone@mergington.edu"})
    assert response.status_code == 404
    assert response.json()["detail"] == "Activity not found"
