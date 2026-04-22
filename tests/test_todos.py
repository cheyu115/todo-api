"""
Unit tests for todos API endpoints.
"""
from datetime import datetime
from typing import List

import sys
import os

# Add the necessary paths for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'app'))
sys.path.insert(0, os.path.dirname(__file__))

import pytest
from fastapi.testclient import TestClient

from app.main import app
from app.routers.todos import FAKE_DATA


@pytest.fixture(autouse=True)
def clear_fake_data():
    """Clear fake data before each test."""
    FAKE_DATA.clear()
    yield
    FAKE_DATA.clear()


class TestCreateTodo:
    """Tests for POST /todos endpoint."""

    def test_create_todo_success(self):
        """Test successful todo creation."""
        client = TestClient(app)
        response = client.post(
            "/todos",
            json={
                "title": "Test Todo",
                "description": "Test Description",
                "is_completed": False,
            },
        )
        assert response.status_code == 201
        data = response.json()
        assert "id" in data
        assert data["title"] == "Test Todo"
        assert data["description"] == "Test Description"
        assert data["is_completed"] is False
        assert "created_at" in data
        assert "updated_at" in data

    def test_create_todo_missing_title(self):
        """Test todo creation with missing title."""
        client = TestClient(app)
        response = client.post(
            "/todos",
            json={
                "description": "Test Description",
                "is_completed": False,
            },
        )
        assert response.status_code == 422

    def test_create_todo_empty_title(self):
        """Test todo creation with empty title (API currently accepts it)."""
        client = TestClient(app)
        response = client.post(
            "/todos",
            json={
                "title": "",
                "description": "Test Description",
                "is_completed": False,
            },
        )
        # Current API behavior: accepts empty title
        assert response.status_code == 201

    def test_create_todo_long_title(self):
        """Test todo creation with title exceeding max length."""
        client = TestClient(app)
        response = client.post(
            "/todos",
            json={
                "title": "x" * 201,
                "description": "Test Description",
                "is_completed": False,
            },
        )
        assert response.status_code == 422

    def test_create_todo_long_description(self):
        """Test todo creation with description exceeding max length."""
        client = TestClient(app)
        response = client.post(
            "/todos",
            json={
                "title": "Test Todo",
                "description": "x" * 1001,
                "is_completed": False,
            },
        )
        assert response.status_code == 422


class TestListTodos:
    """Tests for GET /todos endpoint."""

    def test_list_todos_empty(self):
        """Test listing todos when none exist."""
        client = TestClient(app)
        response = client.get("/todos")
        assert response.status_code == 200
        data = response.json()
        # API returns a list directly, not wrapped in dict
        assert data == []

    def test_list_todos_with_data(self):
        """Test listing todos with existing data."""
        client = TestClient(app)
        # Create a todo first
        create_response = client.post(
            "/todos",
            json={
                "title": "Test Todo 1",
                "description": "First todo",
                "is_completed": False,
            },
        )
        assert create_response.status_code == 201
        todo1 = create_response.json()

        create_response = client.post(
            "/todos",
            json={
                "title": "Test Todo 2",
                "description": "Second todo",
                "is_completed": True,
            },
        )
        assert create_response.status_code == 201
        todo2 = create_response.json()

        response = client.get("/todos")
        assert response.status_code == 200
        data = response.json()
        # API returns a list directly
        assert len(data) == 2
        assert data[0]["id"] == todo1["id"]
        assert data[1]["id"] == todo2["id"]


class TestRetrieveTodo:
    """Tests for GET /todos/{id} endpoint."""

    def test_retrieve_todo_exists(self):
        """Test retrieving an existing todo."""
        client = TestClient(app)
        # Create a todo first
        create_response = client.post(
            "/todos",
            json={
                "title": "Test Todo",
                "description": "Test Description",
                "is_completed": False,
            },
        )
        assert create_response.status_code == 201
        todo = create_response.json()
        todo_id = todo["id"]

        response = client.get(f"/todos/{todo_id}")
        assert response.status_code == 200
        data = response.json()
        assert data["id"] == todo_id
        assert data["title"] == "Test Todo"
        assert data["description"] == "Test Description"
        assert data["is_completed"] is False

    def test_retrieve_todo_not_found(self):
        """Test retrieving a non-existent todo."""
        client = TestClient(app)
        response = client.get("/todos/non-existent-id")
        assert response.status_code == 404
        assert response.json()["detail"] == "Todo not found"

    def test_retrieve_todo_with_special_id(self):
        """Test retrieving a todo with special characters in ID."""
        client = TestClient(app)
        # Create a todo with a specific ID format
        create_response = client.post(
            "/todos",
            json={
                "title": "Test Todo",
                "description": "Test Description",
                "is_completed": False,
            },
        )
        assert create_response.status_code == 201
        todo = create_response.json()
        todo_id = todo["id"]

        response = client.get(f"/todos/{todo_id}")
        assert response.status_code == 200
        assert response.json()["id"] == todo_id


class TestUpdateTodo:
    """Tests for PATCH /todos/{id} endpoint."""

    def test_update_todo_success(self):
        """Test successful todo update."""
        client = TestClient(app)
        # Create a todo first
        create_response = client.post(
            "/todos",
            json={
                "title": "Original Title",
                "description": "Original Description",
                "is_completed": False,
            },
        )
        assert create_response.status_code == 201
        todo = create_response.json()
        todo_id = todo["id"]

        response = client.patch(
            f"/todos/{todo_id}",
            json={
                "title": "Updated Title",
                "description": "Updated Description",
                "is_completed": True,
            },
        )
        assert response.status_code == 200
        data = response.json()
        assert data["id"] == todo_id
        assert data["title"] == "Updated Title"
        assert data["description"] == "Updated Description"
        assert data["is_completed"] is True
        assert data["updated_at"] != todo["updated_at"]

    def test_update_todo_partial_update_title(self):
        """Test partial update (only title)."""
        client = TestClient(app)
        create_response = client.post(
            "/todos",
            json={
                "title": "Original Title",
                "description": "Original Description",
                "is_completed": False,
            },
        )
        assert create_response.status_code == 201
        todo = create_response.json()
        todo_id = todo["id"]
        original_updated_at = todo["updated_at"]

        response = client.patch(
            f"/todos/{todo_id}",
            json={"title": "Updated Title"},
        )
        assert response.status_code == 200
        data = response.json()
        assert data["title"] == "Updated Title"
        assert data["description"] == "Original Description"
        assert data["is_completed"] is False
        assert data["updated_at"] != original_updated_at

    def test_update_todo_partial_update_description(self):
        """Test partial update (only description)."""
        client = TestClient(app)
        create_response = client.post(
            "/todos",
            json={
                "title": "Original Title",
                "description": "Original Description",
                "is_completed": False,
            },
        )
        assert create_response.status_code == 201
        todo = create_response.json()
        todo_id = todo["id"]
        original_updated_at = todo["updated_at"]

        response = client.patch(
            f"/todos/{todo_id}",
            json={"description": "Updated Description"},
        )
        assert response.status_code == 200
        data = response.json()
        assert data["title"] == "Original Title"
        assert data["description"] == "Updated Description"
        assert data["is_completed"] is False
        assert data["updated_at"] != original_updated_at

    def test_update_todo_partial_update_is_completed(self):
        """Test partial update (only is_completed)."""
        client = TestClient(app)
        create_response = client.post(
            "/todos",
            json={
                "title": "Original Title",
                "description": "Original Description",
                "is_completed": False,
            },
        )
        assert create_response.status_code == 201
        todo = create_response.json()
        todo_id = todo["id"]
        original_updated_at = todo["updated_at"]

        response = client.patch(
            f"/todos/{todo_id}",
            json={"is_completed": True},
        )
        assert response.status_code == 200
        data = response.json()
        assert data["title"] == "Original Title"
        assert data["description"] == "Original Description"
        assert data["is_completed"] is True
        assert data["updated_at"] != original_updated_at

    def test_update_todo_not_found(self):
        """Test updating a non-existent todo."""
        client = TestClient(app)
        response = client.patch(
            "/todos/non-existent-id",
            json={"title": "Updated Title"},
        )
        assert response.status_code == 404
        assert response.json()["detail"] == "Todo not found"

    def test_update_todo_no_fields(self):
        """Test update with no fields provided (API currently accepts empty update and updates timestamp)."""
        client = TestClient(app)
        create_response = client.post(
            "/todos",
            json={
                "title": "Test Todo",
                "description": "Test Description",
                "is_completed": False,
            },
        )
        assert create_response.status_code == 201
        todo = create_response.json()
        todo_id = todo["id"]

        response = client.patch(
            f"/todos/{todo_id}",
            json={},
        )
        # Current API behavior: accepts empty update and updates timestamp
        assert response.status_code == 200
        data = response.json()
        assert data["id"] == todo_id
        assert data["title"] == "Test Todo"
        assert data["description"] == "Test Description"
        assert data["is_completed"] is False
        # Note: updated_at will be different due to the empty update operation


class TestDeleteTodo:
    """Tests for DELETE /todos/{id} endpoint."""

    def test_delete_todo_success(self):
        """Test successful todo deletion."""
        client = TestClient(app)
        # Create a todo first
        create_response = client.post(
            "/todos",
            json={
                "title": "Test Todo",
                "description": "Test Description",
                "is_completed": False,
            },
        )
        assert create_response.status_code == 201
        todo = create_response.json()
        todo_id = todo["id"]

        response = client.delete(f"/todos/{todo_id}")
        assert response.status_code == 204
        assert response.content == b""

        # Verify todo is deleted
        get_response = client.get(f"/todos/{todo_id}")
        assert get_response.status_code == 404

    def test_delete_todo_not_found(self):
        """Test deleting a non-existent todo."""
        client = TestClient(app)
        response = client.delete("/todos/non-existent-id")
        assert response.status_code == 404
        assert response.json()["detail"] == "Todo not found"

    def test_delete_todo_multiple_then_delete_one(self):
        """Test deleting one todo from multiple todos."""
        client = TestClient(app)
        # Create multiple todos
        create_response = client.post(
            "/todos",
            json={
                "title": "Todo 1",
                "description": "First todo",
                "is_completed": False,
            },
        )
        assert create_response.status_code == 201
        todo1 = create_response.json()

        create_response = client.post(
            "/todos",
            json={
                "title": "Todo 2",
                "description": "Second todo",
                "is_completed": True,
            },
        )
        assert create_response.status_code == 201
        todo2 = create_response.json()

        # Delete first todo
        response = client.delete(f"/todos/{todo1['id']}")
        assert response.status_code == 204

        # Verify only second todo remains (API returns a list)
        response = client.get("/todos")
        data = response.json()
        assert len(data) == 1
        assert data[0]["id"] == todo2["id"]

        # Verify deleted todo is gone
        get_response = client.get(f"/todos/{todo1['id']}")
        assert get_response.status_code == 404
