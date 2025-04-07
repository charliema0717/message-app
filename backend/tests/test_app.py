import pytest
import sys
import os 

from flask import json

sys.path.append(os.path.dirname(os.path.abspath(__file__)) + "/..")

from app import app

@pytest.fixture
def client():
    app.config["TESTING"] = True
    app.config["JWT_SECRET_KEY"] = "test-secret-key"
    with app.test_client() as client:
        yield client


def test_login_success(client):
    response = client.post('/api/login', json={
        "username": "admin",
        "password": "admin123"
    })
    print("Response Status Code:", response.status_code)
    print("Response Data:", response.json)
    assert response.status_code == 200
    data = json.loads(response.data)
    assert "token" in data
    assert data["user"]["username"] == "admin"
    assert data["user"]["role"] == "admin"


def test_login_failure(client):
    response = client.post('/api/login', json={
        "username": "admin",
        "password": "wrongpassword"
    })
    assert response.status_code == 401
    data = json.loads(response.data)
    assert data["msg"] == "Invalid credentials"


def test_get_messages_without_token(client):
    response = client.get('/api/messages')
    assert response.status_code == 401
    data = json.loads(response.data)
    assert "msg" in data
    assert data["msg"] == "Missing Authorization Header"


def test_get_messages_with_token(client):
    # Login to get a token
    login_response = client.post('/api/login', json={
        "username": "admin",
        "password": "admin123"
    })
    token = json.loads(login_response.data)["token"]

    # Use the token to access messages
    response = client.get('/api/messages', headers={
        "Authorization": f"Bearer {token}"
    })
    assert response.status_code == 200
    data = json.loads(response.data)
    assert isinstance(data, list)
    assert len(data) > 0


def test_add_message_as_admin(client):
    # Login as admin to get a token
    login_response = client.post('/api/login', json={
        "username": "admin",
        "password": "admin123"
    })
    token = json.loads(login_response.data)["token"]

    # Add a new message
    response = client.post('/api/messages', json={
        "message": "This is a test message."
    }, headers={
        "Authorization": f"Bearer {token}"
    })
    assert response.status_code == 201
    data = json.loads(response.data)
    assert "id" in data
    assert data["message"] == "This is a test message."


def test_add_message_as_readonly_user(client):
    # Login as readonly user to get a token
    login_response = client.post('/api/login', json={
        "username": "user",
        "password": "user123"
    })
    token = json.loads(login_response.data)["token"]

    # Try to add a new message
    response = client.post('/api/messages', json={
        "message": "This message should fail."
    }, headers={
        "Authorization": f"Bearer {token}"
    })
    assert response.status_code == 403
    data = json.loads(response.data)
    assert data["msg"] == "Permission denied. Admin role required."


def test_add_message_with_invalid_token(client):
    # Use an invalid token
    response = client.post('/api/messages', json={
        "message": "This message should fail."
    }, headers={
        "Authorization": "Bearer invalid_token"
    })
    assert response.status_code == 422  # Unprocessable Entity
    data = json.loads(response.data)
    assert "msg" in data


def test_add_message_without_content(client):
    # Login as admin to get a token
    login_response = client.post('/api/login', json={
        "username": "admin",
        "password": "admin123"
    })
    token = json.loads(login_response.data)["token"]

    # Try to add a message without content
    response = client.post('/api/messages', json={}, headers={
        "Authorization": f"Bearer {token}"
    })
    assert response.status_code == 400
    data = json.loads(response.data)
    assert data["msg"] == "Message content must be a non-empty string"
