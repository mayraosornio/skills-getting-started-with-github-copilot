import pytest
from fastapi.testclient import TestClient
from src.app import app

client = TestClient(app)

def test_get_activities():
    # Arrange: nothing to set up, just call endpoint
    # Act
    response = client.get("/activities")
    # Assert
    assert response.status_code == 200
    assert isinstance(response.json(), dict)


def test_signup_success():
    # Arrange
    activity_name = list(client.get("/activities").json().keys())[0]
    email = "testuser@mergington.edu"
    # Act
    response = client.post(f"/activities/{activity_name}/signup?email={email}")
    # Assert
    assert response.status_code == 200
    assert "message" in response.json()
    # Clean up
    client.post(f"/activities/{activity_name}/unregister?email={email}")


def test_signup_duplicate():
    # Arrange
    activity_name = list(client.get("/activities").json().keys())[0]
    email = "dupeuser@mergington.edu"
    client.post(f"/activities/{activity_name}/signup?email={email}")
    # Act
    response = client.post(f"/activities/{activity_name}/signup?email={email}")
    # Assert
    assert response.status_code == 400
    assert "Student is already signed up" in response.json()["detail"]
    # Clean up
    client.post(f"/activities/{activity_name}/unregister?email={email}")


def test_signup_invalid_activity():
    # Arrange
    activity_name = "nonexistent"
    email = "invalid@mergington.edu"
    # Act
    response = client.post(f"/activities/{activity_name}/signup?email={email}")
    # Assert
    assert response.status_code == 404


def test_unregister_success():
    # Arrange
    activity_name = list(client.get("/activities").json().keys())[0]
    email = "removeuser@mergington.edu"
    client.post(f"/activities/{activity_name}/signup?email={email}")
    # Act
    response = client.post(f"/activities/{activity_name}/unregister?email={email}")
    # Assert
    assert response.status_code == 200
    assert "message" in response.json()


def test_unregister_not_registered():
    # Arrange
    activity_name = list(client.get("/activities").json().keys())[0]
    email = "notregistered@mergington.edu"
    # Act
    response = client.post(f"/activities/{activity_name}/unregister?email={email}")
    # Assert
    assert response.status_code == 400
    assert "Student is not registered" in response.json()["detail"]


def test_unregister_invalid_activity():
    # Arrange
    activity_name = "nonexistent"
    email = "invalid@mergington.edu"
    # Act
    response = client.post(f"/activities/{activity_name}/unregister?email={email}")
    # Assert
    assert response.status_code == 404
