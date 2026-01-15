"""Tests for ticket API endpoints."""
import pytest


def test_create_ticket(client):
    """Test creating a ticket via API."""
    response = client.post(
        "/api/v1/tickets/",
        json={
            "title": "Test Ticket",
            "description": "Test Description"
        }
    )
    
    assert response.status_code == 201
    data = response.json()
    assert data["title"] == "Test Ticket"
    assert data["description"] == "Test Description"
    assert data["status"] == "pending"
    assert "id" in data


def test_create_ticket_with_tags(client):
    """Test creating a ticket with tags via API."""
    # Create tags first
    tag1_response = client.post(
        "/api/v1/tags/",
        json={"name": "tag1", "color": "#FF0000"}
    )
    tag2_response = client.post(
        "/api/v1/tags/",
        json={"name": "tag2", "color": "#00FF00"}
    )
    tag1_id = tag1_response.json()["id"]
    tag2_id = tag2_response.json()["id"]
    
    # Create ticket with tags
    response = client.post(
        "/api/v1/tickets/",
        json={
            "title": "Test Ticket",
            "description": "Test Description",
            "tag_ids": [tag1_id, tag2_id]
        }
    )
    
    assert response.status_code == 201
    data = response.json()
    assert len(data["tags"]) == 2


def test_get_tickets(client):
    """Test getting all tickets via API."""
    # Create some tickets
    for i in range(3):
        client.post(
            "/api/v1/tickets/",
            json={"title": f"Ticket {i}", "description": ""}
        )
    
    response = client.get("/api/v1/tickets/")
    
    assert response.status_code == 200
    data = response.json()
    assert len(data["tickets"]) == 3
    assert data["total"] == 3


def test_get_ticket(client):
    """Test getting a single ticket via API."""
    # Create a ticket
    create_response = client.post(
        "/api/v1/tickets/",
        json={"title": "Test Ticket", "description": "Test Description"}
    )
    ticket_id = create_response.json()["id"]
    
    # Get the ticket
    response = client.get(f"/api/v1/tickets/{ticket_id}")
    
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == ticket_id
    assert data["title"] == "Test Ticket"


def test_get_ticket_not_found(client):
    """Test getting a non-existent ticket via API."""
    response = client.get("/api/v1/tickets/99999")
    assert response.status_code == 404


def test_get_tickets_with_status_filter(client):
    """Test filtering tickets by status via API."""
    # Create pending tickets
    for i in range(2):
        client.post(
            "/api/v1/tickets/",
            json={"title": f"Pending {i}", "description": ""}
        )
    
    # Create and complete a ticket
    create_response = client.post(
        "/api/v1/tickets/",
        json={"title": "Completed Ticket", "description": ""}
    )
    ticket_id = create_response.json()["id"]
    client.patch(f"/api/v1/tickets/{ticket_id}/complete")
    
    # Get pending tickets
    response = client.get("/api/v1/tickets/?status=pending")
    assert response.status_code == 200
    data = response.json()
    assert data["total"] == 2
    
    # Get completed tickets
    response = client.get("/api/v1/tickets/?status=completed")
    assert response.status_code == 200
    data = response.json()
    assert data["total"] == 1


def test_get_tickets_with_search(client):
    """Test searching tickets via API."""
    client.post(
        "/api/v1/tickets/",
        json={"title": "Python Ticket", "description": "Python description"}
    )
    client.post(
        "/api/v1/tickets/",
        json={"title": "JavaScript Ticket", "description": "JS description"}
    )
    
    response = client.get("/api/v1/tickets/?search=Python")
    assert response.status_code == 200
    data = response.json()
    assert data["total"] == 1
    assert "Python" in data["tickets"][0]["title"]


def test_get_tickets_with_pagination(client):
    """Test pagination via API."""
    # Create 10 tickets
    for i in range(10):
        client.post(
            "/api/v1/tickets/",
            json={"title": f"Ticket {i}", "description": ""}
        )
    
    # Get first page
    response = client.get("/api/v1/tickets/?limit=5&offset=0")
    assert response.status_code == 200
    data = response.json()
    assert len(data["tickets"]) == 5
    assert data["total"] == 10


def test_update_ticket(client):
    """Test updating a ticket via API."""
    # Create a ticket
    create_response = client.post(
        "/api/v1/tickets/",
        json={"title": "Original Title", "description": "Original Description"}
    )
    ticket_id = create_response.json()["id"]
    
    # Update the ticket
    response = client.put(
        f"/api/v1/tickets/{ticket_id}",
        json={"title": "Updated Title", "description": "Updated Description"}
    )
    
    assert response.status_code == 200
    data = response.json()
    assert data["title"] == "Updated Title"
    assert data["description"] == "Updated Description"


def test_update_ticket_not_found(client):
    """Test updating a non-existent ticket via API."""
    response = client.put(
        "/api/v1/tickets/99999",
        json={"title": "Updated Title"}
    )
    assert response.status_code == 404


def test_complete_ticket(client):
    """Test completing a ticket via API."""
    # Create a ticket
    create_response = client.post(
        "/api/v1/tickets/",
        json={"title": "Test Ticket", "description": ""}
    )
    ticket_id = create_response.json()["id"]
    
    # Complete the ticket
    response = client.patch(f"/api/v1/tickets/{ticket_id}/complete")
    
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "completed"
    assert data["completed_at"] is not None


def test_uncomplete_ticket(client):
    """Test uncompleting a ticket via API."""
    # Create and complete a ticket
    create_response = client.post(
        "/api/v1/tickets/",
        json={"title": "Test Ticket", "description": ""}
    )
    ticket_id = create_response.json()["id"]
    client.patch(f"/api/v1/tickets/{ticket_id}/complete")
    
    # Uncomplete the ticket
    response = client.patch(f"/api/v1/tickets/{ticket_id}/uncomplete")
    
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "pending"
    assert data["completed_at"] is None


def test_delete_ticket(client):
    """Test deleting a ticket via API."""
    # Create a ticket
    create_response = client.post(
        "/api/v1/tickets/",
        json={"title": "Test Ticket", "description": ""}
    )
    ticket_id = create_response.json()["id"]
    
    # Delete the ticket
    response = client.delete(f"/api/v1/tickets/{ticket_id}")
    assert response.status_code == 204
    
    # Verify it's deleted
    get_response = client.get(f"/api/v1/tickets/{ticket_id}")
    assert get_response.status_code == 404


def test_add_tags_to_ticket(client):
    """Test adding tags to a ticket via API."""
    # Create tags
    tag1_response = client.post(
        "/api/v1/tags/",
        json={"name": "tag1", "color": "#FF0000"}
    )
    tag2_response = client.post(
        "/api/v1/tags/",
        json={"name": "tag2", "color": "#00FF00"}
    )
    tag1_id = tag1_response.json()["id"]
    tag2_id = tag2_response.json()["id"]
    
    # Create ticket
    create_response = client.post(
        "/api/v1/tickets/",
        json={"title": "Test Ticket", "description": ""}
    )
    ticket_id = create_response.json()["id"]
    
    # Add tags
    response = client.post(
        f"/api/v1/tickets/{ticket_id}/tags",
        json={"tag_ids": [tag1_id, tag2_id]}
    )
    
    assert response.status_code == 200
    data = response.json()
    assert len(data["tags"]) == 2


def test_remove_tag_from_ticket(client):
    """Test removing a tag from a ticket via API."""
    # Create tag
    tag_response = client.post(
        "/api/v1/tags/",
        json={"name": "tag1", "color": "#FF0000"}
    )
    tag_id = tag_response.json()["id"]
    
    # Create ticket with tag
    create_response = client.post(
        "/api/v1/tickets/",
        json={
            "title": "Test Ticket",
            "description": "",
            "tag_ids": [tag_id]
        }
    )
    ticket_id = create_response.json()["id"]
    
    # Remove tag
    response = client.delete(f"/api/v1/tickets/{ticket_id}/tags/{tag_id}")
    
    assert response.status_code == 200
    data = response.json()
    assert len(data["tags"]) == 0
