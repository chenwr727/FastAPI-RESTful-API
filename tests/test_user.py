import sys

import httpx
import pytest
from fastapi.testclient import TestClient

sys.path.append(".")

from main import app

client = TestClient(app)


def assert_404(response: httpx.Response, user_id: int):
    assert response.status_code == 404
    assert response.json()["status"] == "error"
    assert response.json()["message"] == f"User not found with ID: {user_id}"


@pytest.fixture
def user_id():
    """Create a user and return its ID"""
    response = client.post(
        "/users/",
        json={
            "email": "test@example.com",
            "password": "testpassword",
            "username": "testuser",
        },
    )
    assert response.status_code == 200
    data = response.json()["data"]
    user_id = data["id"]
    yield user_id
    response = client.delete(f"/users/{user_id}")
    if response.status_code != 200:
        print(f"Failed to delete user {user_id}: {response.json()}")


def test_read_users():
    """Test reading users"""
    response = client.get("/users/")
    assert response.status_code == 200
    assert response.json()["status"] == "success"
    assert response.json()["message"] == "Users retrieved successfully"
    assert isinstance(response.json()["data"], list)


def test_read_user(user_id: int):
    """Test reading a specific user"""
    response = client.get(f"/users/{user_id}")
    assert response.status_code == 200
    assert response.json()["status"] == "success"
    assert response.json()["message"] == "User retrieved successfully"
    assert response.json()["data"]["id"] == user_id

    response = client.get(f"/users/{user_id + 1}")
    assert_404(response, user_id + 1)


def test_update_user(user_id):
    """Test updating a specific user"""
    response = client.patch(
        f"/users/{user_id}",
        json={
            "email": "updated@example.com",
            "username": "updateduser",
        },
    )
    assert response.status_code == 200
    assert response.json()["status"] == "success"
    assert response.json()["message"] == "User updated successfully"
    assert response.json()["data"]["email"] == "updated@example.com"
    assert response.json()["data"]["username"] == "updateduser"

    response = client.patch(
        f"/users/{user_id + 1}",
        json={
            "email": "updated@example.com",
            "username": "updateduser",
        },
    )
    assert_404(response, user_id + 1)


def test_delete_user(user_id):
    """Test deleting a specific user"""
    response = client.delete(f"/users/{user_id}")
    assert response.status_code == 200
    assert response.json()["status"] == "success"
    assert response.json()["message"] == "User deleted successfully"
    assert response.json()["data"] == {"ok": True}

    response = client.delete(f"/users/{user_id + 1}")
    assert_404(response, user_id + 1)
