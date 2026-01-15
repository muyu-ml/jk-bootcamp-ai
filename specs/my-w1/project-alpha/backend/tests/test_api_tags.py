"""Tests for tag API endpoints."""
import pytest


def test_create_tag(client):
    """Test creating a tag via API."""
    response = client.post(
        "/api/v1/tags/",
        json={"name": "Test Tag", "color": "#FF0000"}
    )
    
    assert response.status_code == 201
    data = response.json()
    assert data["name"] == "Test Tag"
    assert data["color"] == "#FF0000"
    assert "id" in data


def test_create_tag_duplicate_name(client):
    """Test creating a tag with duplicate name via API."""
    # Create first tag
    client.post(
        "/api/v1/tags/",
        json={"name": "Test Tag", "color": "#FF0000"}
    )
    
    # Try to create duplicate
    response = client.post(
        "/api/v1/tags/",
        json={"name": "Test Tag", "color": "#00FF00"}
    )
    
    assert response.status_code == 400


def test_get_tags(client):
    """Test getting all tags via API."""
    # Create some tags
    for i in range(3):
        client.post(
            "/api/v1/tags/",
            json={"name": f"Tag {i}", "color": "#FF0000"}
        )
    
    response = client.get("/api/v1/tags/")
    
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 3


def test_get_tag(client):
    """Test getting a single tag via API."""
    # Create a tag
    create_response = client.post(
        "/api/v1/tags/",
        json={"name": "Test Tag", "color": "#FF0000"}
    )
    tag_id = create_response.json()["id"]
    
    # Get the tag
    response = client.get(f"/api/v1/tags/{tag_id}")
    
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == tag_id
    assert data["name"] == "Test Tag"


def test_get_tag_not_found(client):
    """Test getting a non-existent tag via API."""
    response = client.get("/api/v1/tags/99999")
    assert response.status_code == 404


def test_update_tag(client):
    """Test updating a tag via API."""
    # Create a tag
    create_response = client.post(
        "/api/v1/tags/",
        json={"name": "Original Name", "color": "#FF0000"}
    )
    tag_id = create_response.json()["id"]
    
    # Update the tag
    response = client.put(
        f"/api/v1/tags/{tag_id}",
        json={"name": "Updated Name", "color": "#00FF00"}
    )
    
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "Updated Name"
    assert data["color"] == "#00FF00"


def test_update_tag_not_found(client):
    """Test updating a non-existent tag via API."""
    response = client.put(
        "/api/v1/tags/99999",
        json={"name": "Updated Name"}
    )
    assert response.status_code == 404


def test_delete_tag(client):
    """Test deleting a tag via API."""
    # Create a tag
    create_response = client.post(
        "/api/v1/tags/",
        json={"name": "Test Tag", "color": "#FF0000"}
    )
    tag_id = create_response.json()["id"]
    
    # Delete the tag
    response = client.delete(f"/api/v1/tags/{tag_id}")
    assert response.status_code == 204
    
    # Verify it's deleted
    get_response = client.get(f"/api/v1/tags/{tag_id}")
    assert get_response.status_code == 404


def test_tag_ticket_count(client):
    """Test tag ticket count via API."""
    # Create tag
    tag_response = client.post(
        "/api/v1/tags/",
        json={"name": "Test Tag", "color": "#FF0000"}
    )
    tag_id = tag_response.json()["id"]
    
    # Create tickets with this tag
    for i in range(3):
        client.post(
            "/api/v1/tickets/",
            json={
                "title": f"Ticket {i}",
                "description": "",
                "tag_ids": [tag_id]
            }
        )
    
    # Get tag and check ticket count
    response = client.get(f"/api/v1/tags/{tag_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["ticket_count"] == 3
