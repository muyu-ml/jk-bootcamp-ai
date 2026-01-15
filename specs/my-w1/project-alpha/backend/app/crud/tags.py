"""CRUD operations for tags."""
from sqlalchemy.orm import Session
from sqlalchemy import func
from typing import List, Optional

from app.models.tag import Tag
from app.models.ticket import Ticket
from app.schemas.tag import TagCreate, TagUpdate
from app.utils.color_generator import generate_random_color


def get_tags(db: Session, skip: int = 0, limit: int = 100) -> List[Tag]:
    """Get all tags."""
    return db.query(Tag).offset(skip).limit(limit).all()


def get_tag_ticket_count(db: Session, tag_id: int) -> int:
    """
    Get the count of tickets associated with a tag.
    Uses a SQL query to avoid N+1 problem.

    Args:
        db: Database session
        tag_id: ID of the tag

    Returns:
        Number of tickets associated with the tag
    """
    from app.models.tag import ticket_tags
    count = (
        db.query(func.count(ticket_tags.c.ticket_id))
        .filter(ticket_tags.c.tag_id == tag_id)
        .scalar()
    )
    return count or 0


def get_tag(db: Session, tag_id: int) -> Optional[Tag]:
    """Get a tag by ID."""
    return db.query(Tag).filter(Tag.id == tag_id).first()


def get_tag_by_name(db: Session, name: str) -> Optional[Tag]:
    """Get a tag by name."""
    return db.query(Tag).filter(Tag.name == name).first()


def create_tag(db: Session, tag: TagCreate) -> Tag:
    """
    Create a new tag.

    Args:
        db: Database session
        tag: Tag creation data

    Returns:
        Created tag
    """
    # Generate color if not provided
    color = tag.color
    if not color:
        color = generate_random_color()

    db_tag = Tag(name=tag.name, color=color)
    db.add(db_tag)
    db.commit()
    db.refresh(db_tag)
    return db_tag


def update_tag(db: Session, tag_id: int, tag_update: TagUpdate) -> Optional[Tag]:
    """
    Update a tag.

    Args:
        db: Database session
        tag_id: ID of the tag to update
        tag_update: Tag update data

    Returns:
        Updated tag or None if not found
    """
    db_tag = get_tag(db, tag_id)
    if not db_tag:
        return None

    if tag_update.name is not None:
        db_tag.name = tag_update.name
    if tag_update.color is not None:
        db_tag.color = tag_update.color

    db.commit()
    db.refresh(db_tag)
    return db_tag


def delete_tag(db: Session, tag_id: int) -> bool:
    """
    Delete a tag.

    Args:
        db: Database session
        tag_id: ID of the tag to delete

    Returns:
        True if deleted, False if not found
    """
    db_tag = get_tag(db, tag_id)
    if not db_tag:
        return False

    db.delete(db_tag)
    db.commit()
    return True
