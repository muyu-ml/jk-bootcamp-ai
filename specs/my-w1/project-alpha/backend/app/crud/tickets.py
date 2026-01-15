"""CRUD operations for tickets."""
from sqlalchemy.orm import Session, joinedload
from sqlalchemy import or_, and_, func
from typing import List, Optional, Tuple
from datetime import datetime, timezone

from app.models.ticket import Ticket, TicketStatus
from app.models.tag import Tag
from app.schemas.ticket import TicketCreate, TicketUpdate


def get_tickets(
    db: Session,
    status: Optional[str] = None,
    tag_ids: Optional[List[int]] = None,
    search: Optional[str] = None,
    sort_by: Optional[str] = None,
    order: Optional[str] = "asc",
    limit: Optional[int] = None,
    offset: Optional[int] = 0,
) -> Tuple[List[Ticket], int]:
    """
    Get tickets with optional filtering, searching, sorting, and pagination.

    Args:
        db: Database session
        status: Filter by status (pending/completed)
        tag_ids: Filter by tag IDs (comma-separated string or list)
        search: Search in title and description
        sort_by: Field to sort by (created_at, updated_at, completed_at)
        order: Sort order (asc/desc)
        limit: Maximum number of results
        offset: Number of results to skip

    Returns:
        Tuple of (list of tickets, total count)
    """
    # Base query with eager loading to avoid N+1 queries
    query = db.query(Ticket).options(joinedload(Ticket.tags))

    # Count query (without pagination and eager loading for better performance)
    count_query = db.query(func.count(Ticket.id))

    # Filter by status
    if status:
        try:
            ticket_status = TicketStatus(status)
            query = query.filter(Ticket.status == ticket_status.value)
            count_query = count_query.filter(Ticket.status == ticket_status.value)
        except ValueError:
            pass  # Invalid status, ignore filter

    # Filter by tags
    if tag_ids:
        if isinstance(tag_ids, str):
            tag_ids = [int(tid.strip()) for tid in tag_ids.split(",") if tid.strip()]
        query = query.join(Ticket.tags).filter(Tag.id.in_(tag_ids)).distinct()
        count_query = count_query.join(Ticket.tags).filter(Tag.id.in_(tag_ids)).distinct()

    # Search in title and description
    if search:
        search_pattern = f"%{search}%"
        query = query.filter(
            or_(
                Ticket.title.ilike(search_pattern),
                Ticket.description.ilike(search_pattern),
            )
        )
        count_query = count_query.filter(
            or_(
                Ticket.title.ilike(search_pattern),
                Ticket.description.ilike(search_pattern),
            )
        )

    # Get total count before pagination
    total = count_query.scalar()

    # Sorting
    if sort_by:
        if sort_by == "created_at":
            sort_field = Ticket.created_at
        elif sort_by == "updated_at":
            sort_field = Ticket.updated_at
        elif sort_by == "completed_at":
            sort_field = Ticket.completed_at
        else:
            sort_field = Ticket.created_at

        if order and order.lower() == "desc":
            query = query.order_by(sort_field.desc())
        else:
            query = query.order_by(sort_field.asc())
    else:
        # Default sorting by created_at desc
        query = query.order_by(Ticket.created_at.desc())

    # Pagination
    if offset:
        query = query.offset(offset)
    if limit:
        query = query.limit(limit)

    return query.all(), total


def get_ticket(db: Session, ticket_id: int) -> Optional[Ticket]:
    """Get a ticket by ID with eager loading of tags."""
    return (
        db.query(Ticket)
        .options(joinedload(Ticket.tags))
        .filter(Ticket.id == ticket_id)
        .first()
    )


def create_ticket(db: Session, ticket: TicketCreate, tag_ids: Optional[List[int]] = None) -> Ticket:
    """
    Create a new ticket.

    Args:
        db: Database session
        ticket: Ticket creation data
        tag_ids: Optional list of tag IDs to associate with the ticket

    Returns:
        Created ticket
    """
    # Create ticket
    db_ticket = Ticket(
        title=ticket.title,
        description=ticket.description,
        status=TicketStatus.PENDING.value,
    )

    # Associate tags if provided
    if tag_ids:
        tags = db.query(Tag).filter(Tag.id.in_(tag_ids)).all()
        db_ticket.tags = tags

    db.add(db_ticket)
    db.commit()
    db.refresh(db_ticket)
    # Reload with tags to ensure they're loaded
    return get_ticket(db, db_ticket.id)


def update_ticket(db: Session, ticket_id: int, ticket_update: TicketUpdate) -> Optional[Ticket]:
    """
    Update a ticket.

    Args:
        db: Database session
        ticket_id: ID of the ticket to update
        ticket_update: Ticket update data

    Returns:
        Updated ticket or None if not found
    """
    db_ticket = get_ticket(db, ticket_id)
    if not db_ticket:
        return None

    if ticket_update.title is not None:
        db_ticket.title = ticket_update.title
    if ticket_update.description is not None:
        db_ticket.description = ticket_update.description

    db.commit()
    db.refresh(db_ticket)
    # Reload with tags to ensure they're loaded
    return get_ticket(db, db_ticket.id)


def complete_ticket(db: Session, ticket_id: int) -> Optional[Ticket]:
    """
    Mark a ticket as completed.

    Args:
        db: Database session
        ticket_id: ID of the ticket to complete

    Returns:
        Updated ticket or None if not found
    """
    db_ticket = get_ticket(db, ticket_id)
    if not db_ticket:
        return None

    db_ticket.status = TicketStatus.COMPLETED.value
    db_ticket.completed_at = datetime.now(timezone.utc)

    db.commit()
    db.refresh(db_ticket)
    # Reload with tags to ensure they're loaded
    return get_ticket(db, db_ticket.id)


def uncomplete_ticket(db: Session, ticket_id: int) -> Optional[Ticket]:
    """
    Mark a ticket as pending (uncomplete).

    Args:
        db: Database session
        ticket_id: ID of the ticket to uncomplete

    Returns:
        Updated ticket or None if not found
    """
    db_ticket = get_ticket(db, ticket_id)
    if not db_ticket:
        return None

    db_ticket.status = TicketStatus.PENDING.value
    db_ticket.completed_at = None

    db.commit()
    db.refresh(db_ticket)
    # Reload with tags to ensure they're loaded
    return get_ticket(db, db_ticket.id)


def delete_ticket(db: Session, ticket_id: int) -> bool:
    """
    Delete a ticket.

    Args:
        db: Database session
        ticket_id: ID of the ticket to delete

    Returns:
        True if deleted, False if not found
    """
    db_ticket = get_ticket(db, ticket_id)
    if not db_ticket:
        return False

    db.delete(db_ticket)
    db.commit()
    return True


def add_tags_to_ticket(db: Session, ticket_id: int, tag_ids: List[int]) -> Optional[Ticket]:
    """
    Add tags to a ticket.

    Args:
        db: Database session
        ticket_id: ID of the ticket
        tag_ids: List of tag IDs to add

    Returns:
        Updated ticket or None if not found
    """
    db_ticket = get_ticket(db, ticket_id)
    if not db_ticket:
        return None

    tags = db.query(Tag).filter(Tag.id.in_(tag_ids)).all()
    # Add tags (avoid duplicates)
    for tag in tags:
        if tag not in db_ticket.tags:
            db_ticket.tags.append(tag)

    db.commit()
    db.refresh(db_ticket)
    # Reload with tags to ensure they're loaded
    return get_ticket(db, db_ticket.id)


def remove_tag_from_ticket(db: Session, ticket_id: int, tag_id: int) -> Optional[Ticket]:
    """
    Remove a tag from a ticket.

    Args:
        db: Database session
        ticket_id: ID of the ticket
        tag_id: ID of the tag to remove

    Returns:
        Updated ticket or None if not found
    """
    db_ticket = get_ticket(db, ticket_id)
    if not db_ticket:
        return None

    tag = db.query(Tag).filter(Tag.id == tag_id).first()
    if tag and tag in db_ticket.tags:
        db_ticket.tags.remove(tag)
        db.commit()
        db.refresh(db_ticket)
        # Reload with tags to ensure they're loaded
        return get_ticket(db, db_ticket.id)

    return db_ticket
