"""Tests for ticket CRUD operations."""
import pytest
from datetime import datetime, timezone

from app.crud import tickets as crud_tickets
from app.schemas.ticket import TicketCreate, TicketUpdate
from app.models.ticket import TicketStatus


def test_create_ticket(db_session):
    """Test creating a ticket."""
    ticket_data = TicketCreate(
        title="Test Ticket",
        description="Test Description"
    )
    
    ticket = crud_tickets.create_ticket(db=db_session, ticket=ticket_data)
    
    assert ticket.id is not None
    assert ticket.title == "Test Ticket"
    assert ticket.description == "Test Description"
    assert ticket.status == TicketStatus.PENDING.value
    assert ticket.created_at is not None


def test_create_ticket_with_tags(db_session):
    """Test creating a ticket with tags."""
    from app.models.tag import Tag
    
    # Create tags first
    tag1 = Tag(name="tag1", color="#FF0000")
    tag2 = Tag(name="tag2", color="#00FF00")
    db_session.add(tag1)
    db_session.add(tag2)
    db_session.commit()
    
    ticket_data = TicketCreate(
        title="Test Ticket",
        description="Test Description"
    )
    
    ticket = crud_tickets.create_ticket(
        db=db_session,
        ticket=ticket_data,
        tag_ids=[tag1.id, tag2.id]
    )
    
    assert len(ticket.tags) == 2
    assert tag1 in ticket.tags
    assert tag2 in ticket.tags


def test_get_ticket(db_session):
    """Test getting a ticket by ID."""
    ticket_data = TicketCreate(
        title="Test Ticket",
        description="Test Description"
    )
    
    created_ticket = crud_tickets.create_ticket(db=db_session, ticket=ticket_data)
    retrieved_ticket = crud_tickets.get_ticket(db=db_session, ticket_id=created_ticket.id)
    
    assert retrieved_ticket is not None
    assert retrieved_ticket.id == created_ticket.id
    assert retrieved_ticket.title == "Test Ticket"


def test_get_ticket_not_found(db_session):
    """Test getting a non-existent ticket."""
    ticket = crud_tickets.get_ticket(db=db_session, ticket_id=99999)
    assert ticket is None


def test_get_tickets(db_session):
    """Test getting all tickets."""
    # Create multiple tickets
    for i in range(5):
        ticket_data = TicketCreate(
            title=f"Ticket {i}",
            description=f"Description {i}"
        )
        crud_tickets.create_ticket(db=db_session, ticket=ticket_data)
    
    tickets, total = crud_tickets.get_tickets(db=db_session)
    
    assert len(tickets) == 5
    assert total == 5


def test_get_tickets_with_status_filter(db_session):
    """Test getting tickets filtered by status."""
    # Create pending tickets
    for i in range(3):
        ticket_data = TicketCreate(title=f"Pending {i}", description="")
        crud_tickets.create_ticket(db=db_session, ticket=ticket_data)
    
    # Create completed tickets
    for i in range(2):
        ticket_data = TicketCreate(title=f"Completed {i}", description="")
        ticket = crud_tickets.create_ticket(db=db_session, ticket=ticket_data)
        crud_tickets.complete_ticket(db=db_session, ticket_id=ticket.id)
    
    # Get pending tickets
    pending_tickets, pending_total = crud_tickets.get_tickets(
        db=db_session,
        status="pending"
    )
    assert pending_total == 3
    
    # Get completed tickets
    completed_tickets, completed_total = crud_tickets.get_tickets(
        db=db_session,
        status="completed"
    )
    assert completed_total == 2


def test_get_tickets_with_search(db_session):
    """Test searching tickets."""
    crud_tickets.create_ticket(
        db=db_session,
        ticket=TicketCreate(title="Python Ticket", description="Python description")
    )
    crud_tickets.create_ticket(
        db=db_session,
        ticket=TicketCreate(title="JavaScript Ticket", description="JS description")
    )
    
    tickets, total = crud_tickets.get_tickets(db=db_session, search="Python")
    assert total == 1
    assert tickets[0].title == "Python Ticket"


def test_get_tickets_with_pagination(db_session):
    """Test pagination."""
    # Create 10 tickets
    for i in range(10):
        ticket_data = TicketCreate(title=f"Ticket {i}", description="")
        crud_tickets.create_ticket(db=db_session, ticket=ticket_data)
    
    # Get first page
    tickets_page1, total = crud_tickets.get_tickets(
        db=db_session,
        limit=5,
        offset=0
    )
    assert len(tickets_page1) == 5
    assert total == 10
    
    # Get second page
    tickets_page2, total = crud_tickets.get_tickets(
        db=db_session,
        limit=5,
        offset=5
    )
    assert len(tickets_page2) == 5
    assert total == 10


def test_update_ticket(db_session):
    """Test updating a ticket."""
    ticket_data = TicketCreate(title="Original Title", description="Original Description")
    ticket = crud_tickets.create_ticket(db=db_session, ticket=ticket_data)
    
    update_data = TicketUpdate(title="Updated Title", description="Updated Description")
    updated_ticket = crud_tickets.update_ticket(
        db=db_session,
        ticket_id=ticket.id,
        ticket_update=update_data
    )
    
    assert updated_ticket.title == "Updated Title"
    assert updated_ticket.description == "Updated Description"


def test_update_ticket_not_found(db_session):
    """Test updating a non-existent ticket."""
    update_data = TicketUpdate(title="Updated Title")
    result = crud_tickets.update_ticket(
        db=db_session,
        ticket_id=99999,
        ticket_update=update_data
    )
    assert result is None


def test_complete_ticket(db_session):
    """Test completing a ticket."""
    ticket_data = TicketCreate(title="Test Ticket", description="")
    ticket = crud_tickets.create_ticket(db=db_session, ticket=ticket_data)
    
    assert ticket.status == TicketStatus.PENDING.value
    assert ticket.completed_at is None
    
    completed_ticket = crud_tickets.complete_ticket(db=db_session, ticket_id=ticket.id)
    
    assert completed_ticket.status == TicketStatus.COMPLETED.value
    assert completed_ticket.completed_at is not None


def test_uncomplete_ticket(db_session):
    """Test uncompleting a ticket."""
    ticket_data = TicketCreate(title="Test Ticket", description="")
    ticket = crud_tickets.create_ticket(db=db_session, ticket=ticket_data)
    crud_tickets.complete_ticket(db=db_session, ticket_id=ticket.id)
    
    uncompleted_ticket = crud_tickets.uncomplete_ticket(db=db_session, ticket_id=ticket.id)
    
    assert uncompleted_ticket.status == TicketStatus.PENDING.value
    assert uncompleted_ticket.completed_at is None


def test_delete_ticket(db_session):
    """Test deleting a ticket."""
    ticket_data = TicketCreate(title="Test Ticket", description="")
    ticket = crud_tickets.create_ticket(db=db_session, ticket=ticket_data)
    
    result = crud_tickets.delete_ticket(db=db_session, ticket_id=ticket.id)
    assert result is True
    
    deleted_ticket = crud_tickets.get_ticket(db=db_session, ticket_id=ticket.id)
    assert deleted_ticket is None


def test_delete_ticket_not_found(db_session):
    """Test deleting a non-existent ticket."""
    result = crud_tickets.delete_ticket(db=db_session, ticket_id=99999)
    assert result is False


def test_add_tags_to_ticket(db_session):
    """Test adding tags to a ticket."""
    from app.models.tag import Tag
    
    # Create tags
    tag1 = Tag(name="tag1", color="#FF0000")
    tag2 = Tag(name="tag2", color="#00FF00")
    db_session.add(tag1)
    db_session.add(tag2)
    db_session.commit()
    
    # Create ticket
    ticket_data = TicketCreate(title="Test Ticket", description="")
    ticket = crud_tickets.create_ticket(db=db_session, ticket=ticket_data)
    
    # Add tags
    updated_ticket = crud_tickets.add_tags_to_ticket(
        db=db_session,
        ticket_id=ticket.id,
        tag_ids=[tag1.id, tag2.id]
    )
    
    assert len(updated_ticket.tags) == 2


def test_remove_tag_from_ticket(db_session):
    """Test removing a tag from a ticket."""
    from app.models.tag import Tag
    
    # Create tags
    tag1 = Tag(name="tag1", color="#FF0000")
    tag2 = Tag(name="tag2", color="#00FF00")
    db_session.add(tag1)
    db_session.add(tag2)
    db_session.commit()
    
    # Create ticket with tags
    ticket_data = TicketCreate(title="Test Ticket", description="")
    ticket = crud_tickets.create_ticket(
        db=db_session,
        ticket=ticket_data,
        tag_ids=[tag1.id, tag2.id]
    )
    
    # Remove one tag
    updated_ticket = crud_tickets.remove_tag_from_ticket(
        db=db_session,
        ticket_id=ticket.id,
        tag_id=tag1.id
    )
    
    assert len(updated_ticket.tags) == 1
    assert tag2 in updated_ticket.tags
    assert tag1 not in updated_ticket.tags
