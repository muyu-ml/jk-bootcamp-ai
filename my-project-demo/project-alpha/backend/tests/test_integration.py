"""Integration tests for the full API workflow."""
import pytest


def test_full_ticket_workflow(client):
    """Test complete ticket lifecycle."""
    # 1. Create tags
    tag1_response = client.post(
        "/api/v1/tags/",
        json={"name": "urgent", "color": "#FF0000"}
    )
    tag2_response = client.post(
        "/api/v1/tags/",
        json={"name": "bug", "color": "#00FF00"}
    )
    tag1_id = tag1_response.json()["id"]
    tag2_id = tag2_response.json()["id"]
    
    # 2. Create ticket with tags
    ticket_response = client.post(
        "/api/v1/tickets/",
        json={
            "title": "Fix critical bug",
            "description": "This is a critical bug that needs immediate attention",
            "tag_ids": [tag1_id, tag2_id]
        }
    )
    assert ticket_response.status_code == 201
    ticket_id = ticket_response.json()["id"]
    assert len(ticket_response.json()["tags"]) == 2
    
    # 3. Get ticket
    get_response = client.get(f"/api/v1/tickets/{ticket_id}")
    assert get_response.status_code == 200
    assert get_response.json()["title"] == "Fix critical bug"
    
    # 4. Update ticket
    update_response = client.put(
        f"/api/v1/tickets/{ticket_id}",
        json={
            "title": "Fix critical bug - Updated",
            "description": "Updated description"
        }
    )
    assert update_response.status_code == 200
    assert update_response.json()["title"] == "Fix critical bug - Updated"
    
    # 5. Complete ticket
    complete_response = client.patch(f"/api/v1/tickets/{ticket_id}/complete")
    assert complete_response.status_code == 200
    assert complete_response.json()["status"] == "completed"
    assert complete_response.json()["completed_at"] is not None
    
    # 6. Filter by status
    completed_tickets = client.get("/api/v1/tickets/?status=completed")
    assert completed_tickets.status_code == 200
    assert completed_tickets.json()["total"] >= 1
    
    # 7. Search tickets
    search_response = client.get("/api/v1/tickets/?search=critical")
    assert search_response.status_code == 200
    assert search_response.json()["total"] >= 1
    
    # 8. Filter by tag
    tag_filter_response = client.get(f"/api/v1/tickets/?tag_ids={tag1_id}")
    assert tag_filter_response.status_code == 200
    assert tag_filter_response.json()["total"] >= 1
    
    # 9. Remove tag from ticket
    remove_tag_response = client.delete(f"/api/v1/tickets/{ticket_id}/tags/{tag1_id}")
    assert remove_tag_response.status_code == 200
    assert len(remove_tag_response.json()["tags"]) == 1
    
    # 10. Uncomplete ticket
    uncomplete_response = client.patch(f"/api/v1/tickets/{ticket_id}/uncomplete")
    assert uncomplete_response.status_code == 200
    assert uncomplete_response.json()["status"] == "pending"
    
    # 11. Delete ticket
    delete_response = client.delete(f"/api/v1/tickets/{ticket_id}")
    assert delete_response.status_code == 204
    
    # 12. Verify deletion
    get_deleted_response = client.get(f"/api/v1/tickets/{ticket_id}")
    assert get_deleted_response.status_code == 404


def test_tag_management_workflow(client):
    """Test complete tag management workflow."""
    # 1. Create tag
    create_response = client.post(
        "/api/v1/tags/",
        json={"name": "feature", "color": "#0000FF"}
    )
    assert create_response.status_code == 201
    tag_id = create_response.json()["id"]
    
    # 2. Get tag
    get_response = client.get(f"/api/v1/tags/{tag_id}")
    assert get_response.status_code == 200
    assert get_response.json()["name"] == "feature"
    
    # 3. Create ticket with tag
    ticket_response = client.post(
        "/api/v1/tickets/",
        json={
            "title": "New feature",
            "description": "Implement new feature",
            "tag_ids": [tag_id]
        }
    )
    assert ticket_response.status_code == 201
    ticket_id = ticket_response.json()["id"]
    
    # 4. Check tag ticket count
    tag_response = client.get(f"/api/v1/tags/{tag_id}")
    assert tag_response.status_code == 200
    assert tag_response.json()["ticket_count"] == 1
    
    # 5. Update tag
    update_response = client.put(
        f"/api/v1/tags/{tag_id}",
        json={"name": "feature-updated", "color": "#0000FF"}
    )
    assert update_response.status_code == 200
    assert update_response.json()["name"] == "feature-updated"
    
    # 6. Delete tag (should cascade delete associations)
    delete_response = client.delete(f"/api/v1/tags/{tag_id}")
    assert delete_response.status_code == 204
    
    # 7. Verify tag deletion
    get_deleted_response = client.get(f"/api/v1/tags/{tag_id}")
    assert get_deleted_response.status_code == 404
    
    # 8. Verify ticket still exists (tags removed)
    ticket_check = client.get(f"/api/v1/tickets/{ticket_id}")
    assert ticket_check.status_code == 200
    assert len(ticket_check.json()["tags"]) == 0
