"""Tests for tag CRUD operations."""
import pytest

from app.crud import tags as crud_tags
from app.schemas.tag import TagCreate, TagUpdate


def test_create_tag(db_session):
    """Test creating a tag."""
    tag_data = TagCreate(name="Test Tag", color="#FF0000")
    
    tag = crud_tags.create_tag(db=db_session, tag=tag_data)
    
    assert tag.id is not None
    assert tag.name == "Test Tag"
    assert tag.color == "#FF0000"
    assert tag.created_at is not None


def test_create_tag_without_color(db_session):
    """Test creating a tag without color (should auto-generate)."""
    tag_data = TagCreate(name="Test Tag")
    
    tag = crud_tags.create_tag(db=db_session, tag=tag_data)
    
    assert tag.color is not None
    assert len(tag.color) == 7  # Hex color format #RRGGBB
    assert tag.color.startswith("#")


def test_get_tag(db_session):
    """Test getting a tag by ID."""
    tag_data = TagCreate(name="Test Tag", color="#FF0000")
    created_tag = crud_tags.create_tag(db=db_session, tag=tag_data)
    
    retrieved_tag = crud_tags.get_tag(db=db_session, tag_id=created_tag.id)
    
    assert retrieved_tag is not None
    assert retrieved_tag.id == created_tag.id
    assert retrieved_tag.name == "Test Tag"


def test_get_tag_not_found(db_session):
    """Test getting a non-existent tag."""
    tag = crud_tags.get_tag(db=db_session, tag_id=99999)
    assert tag is None


def test_get_tag_by_name(db_session):
    """Test getting a tag by name."""
    tag_data = TagCreate(name="Test Tag", color="#FF0000")
    created_tag = crud_tags.create_tag(db=db_session, tag=tag_data)
    
    retrieved_tag = crud_tags.get_tag_by_name(db=db_session, name="Test Tag")
    
    assert retrieved_tag is not None
    assert retrieved_tag.id == created_tag.id


def test_get_tags(db_session):
    """Test getting all tags."""
    # Create multiple tags
    for i in range(5):
        tag_data = TagCreate(name=f"Tag {i}", color="#FF0000")
        crud_tags.create_tag(db=db_session, tag=tag_data)
    
    tags = crud_tags.get_tags(db=db_session)
    
    assert len(tags) == 5


def test_get_tags_with_pagination(db_session):
    """Test pagination for tags."""
    # Create 10 tags
    for i in range(10):
        tag_data = TagCreate(name=f"Tag {i}", color="#FF0000")
        crud_tags.create_tag(db=db_session, tag=tag_data)
    
    # Get first page
    tags_page1 = crud_tags.get_tags(db=db_session, skip=0, limit=5)
    assert len(tags_page1) == 5
    
    # Get second page
    tags_page2 = crud_tags.get_tags(db=db_session, skip=5, limit=5)
    assert len(tags_page2) == 5


def test_update_tag(db_session):
    """Test updating a tag."""
    tag_data = TagCreate(name="Original Name", color="#FF0000")
    tag = crud_tags.create_tag(db=db_session, tag=tag_data)
    
    update_data = TagUpdate(name="Updated Name", color="#00FF00")
    updated_tag = crud_tags.update_tag(
        db=db_session,
        tag_id=tag.id,
        tag_update=update_data
    )
    
    assert updated_tag.name == "Updated Name"
    assert updated_tag.color == "#00FF00"


def test_update_tag_partial(db_session):
    """Test partial update of a tag."""
    tag_data = TagCreate(name="Original Name", color="#FF0000")
    tag = crud_tags.create_tag(db=db_session, tag=tag_data)
    
    # Update only name
    update_data = TagUpdate(name="Updated Name")
    updated_tag = crud_tags.update_tag(
        db=db_session,
        tag_id=tag.id,
        tag_update=update_data
    )
    
    assert updated_tag.name == "Updated Name"
    assert updated_tag.color == "#FF0000"  # Unchanged


def test_update_tag_not_found(db_session):
    """Test updating a non-existent tag."""
    update_data = TagUpdate(name="Updated Name")
    result = crud_tags.update_tag(
        db=db_session,
        tag_id=99999,
        tag_update=update_data
    )
    assert result is None


def test_delete_tag(db_session):
    """Test deleting a tag."""
    tag_data = TagCreate(name="Test Tag", color="#FF0000")
    tag = crud_tags.create_tag(db=db_session, tag=tag_data)
    
    result = crud_tags.delete_tag(db=db_session, tag_id=tag.id)
    assert result is True
    
    deleted_tag = crud_tags.get_tag(db=db_session, tag_id=tag.id)
    assert deleted_tag is None


def test_delete_tag_not_found(db_session):
    """Test deleting a non-existent tag."""
    result = crud_tags.delete_tag(db=db_session, tag_id=99999)
    assert result is False


def test_get_tag_ticket_count(db_session):
    """Test getting ticket count for a tag."""
    from app.crud import tickets as crud_tickets
    from app.schemas.ticket import TicketCreate
    
    # Create tag
    tag_data = TagCreate(name="Test Tag", color="#FF0000")
    tag = crud_tags.create_tag(db=db_session, tag=tag_data)
    
    # Create tickets with this tag
    for i in range(3):
        ticket_data = TicketCreate(title=f"Ticket {i}", description="")
        crud_tickets.create_ticket(
            db=db_session,
            ticket=ticket_data,
            tag_ids=[tag.id]
        )
    
    count = crud_tags.get_tag_ticket_count(db=db_session, tag_id=tag.id)
    assert count == 3
