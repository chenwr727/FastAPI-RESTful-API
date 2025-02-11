import sys

import httpx
import pytest
from fastapi.testclient import TestClient
from test_user import assert_404 as assert_404_user

sys.path.append(".")
from main import app

client = TestClient(app)


def assert_404(response: httpx.Response, item_id: int):
    assert response.status_code == 404
    assert response.json()["status"] == "error"
    assert response.json()["message"] == f"Item not found with ID: {item_id}"


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


@pytest.fixture
def item_id(user_id):
    """Create an item and return its ID"""
    response = client.post(
        f"/items/?owner_id={user_id}",
        json={"title": "Test Item", "description": "This is a test item"},
    )
    assert response.status_code == 200
    data = response.json()["data"]
    item_id = data["id"]
    yield item_id
    response = client.delete(f"/items/{item_id}")
    if response.status_code != 200:
        print(f"Failed to delete item {item_id}: {response.json()}")


def test_create_item(user_id):
    """Test creating a new item"""
    response = client.post(
        f"/items/?owner_id={user_id}",
        json={"title": "New Item", "description": "This is a new item"},
    )
    assert response.status_code == 200
    data = response.json()["data"]
    assert data["title"] == "New Item"
    assert data["description"] == "This is a new item"
    assert data["owner_id"] == user_id

    response = client.post(
        f"/items/?owner_id={user_id + 1}",
        json={"title": "New Item", "description": "This is a new item"},
    )
    assert_404_user(response, user_id + 1)


def test_read_items():
    """Test reading a list of items"""
    response = client.get("/items/")
    assert response.status_code == 200
    assert response.json()["status"] == "success"
    assert response.json()["message"] == "Items retrieved successfully"
    assert isinstance(response.json()["data"], list)


def test_read_item(item_id):
    """Test reading a specific item"""
    response = client.get(f"/items/{item_id}")
    assert response.status_code == 200
    assert response.json()["status"] == "success"
    assert response.json()["message"] == "Item retrieved successfully"
    data = response.json()["data"]
    assert data["id"] == item_id

    response = client.get(f"/items/{item_id + 1}")
    assert_404(response, item_id + 1)


def test_update_item(item_id):
    """Test updating a specific item"""
    response = client.patch(
        f"/items/{item_id}",
        json={
            "title": "Updated Item",
            "description": "This is an updated item",
        },
    )
    assert response.status_code == 200
    assert response.json()["status"] == "success"
    assert response.json()["message"] == "Item updated successfully"
    data = response.json()["data"]
    assert data["title"] == "Updated Item"
    assert data["description"] == "This is an updated item"

    response = client.patch(
        f"/items/{item_id + 1}",
        json={
            "title": "Updated Item",
            "description": "This is an updated item",
        },
    )
    assert_404(response, item_id + 1)


def test_delete_item(item_id):
    """Test deleting a specific item"""
    response = client.delete(f"/items/{item_id}")
    assert response.status_code == 200
    assert response.json()["status"] == "success"
    assert response.json()["message"] == "Item deleted successfully"
    assert response.json()["data"] == {"ok": True}

    response = client.delete(f"/items/{item_id + 1}")
    assert_404(response, item_id + 1)
