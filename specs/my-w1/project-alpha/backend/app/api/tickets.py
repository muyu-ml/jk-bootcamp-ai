"""Ticket API routes."""
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from pydantic import BaseModel

from app.database import get_db
from app.schemas.ticket import TicketCreate, TicketUpdate, TicketResponse, TicketListResponse
from app.crud import tickets as crud_tickets

router = APIRouter()


class TagIdsRequest(BaseModel):
    """Request model for adding tags to a ticket."""
    tag_ids: List[int]


@router.get("/", response_model=TicketListResponse)
def get_tickets(
    status: Optional[str] = Query(None, description="Filter by status (pending/completed)"),
    tag_ids: Optional[str] = Query(None, description="Filter by tag IDs (comma-separated)"),
    search: Optional[str] = Query(None, description="Search in title and description"),
    sort_by: Optional[str] = Query(None, description="Sort by field (created_at, updated_at, completed_at)"),
    order: Optional[str] = Query("asc", description="Sort order (asc/desc)"),
    limit: Optional[int] = Query(None, ge=1, description="Maximum number of results"),
    offset: Optional[int] = Query(0, ge=0, description="Number of results to skip"),
    db: Session = Depends(get_db),
):
    """Get all tickets with optional filtering, searching, sorting, and pagination."""
    # Convert tag_ids string to list if provided
    tag_ids_list = None
    if tag_ids:
        tag_ids_list = [int(tid.strip()) for tid in tag_ids.split(",") if tid.strip()]

    db_tickets, total = crud_tickets.get_tickets(
        db=db,
        status=status,
        tag_ids=tag_ids_list,
        search=search,
        sort_by=sort_by,
        order=order,
        limit=limit,
        offset=offset,
    )
    return TicketListResponse(
        tickets=db_tickets,
        total=total,
        limit=limit,
        offset=offset,
    )


@router.get("/{ticket_id}", response_model=TicketResponse)
def get_ticket(ticket_id: int, db: Session = Depends(get_db)):
    """Get a ticket by ID."""
    db_ticket = crud_tickets.get_ticket(db, ticket_id=ticket_id)
    if db_ticket is None:
        raise HTTPException(status_code=404, detail="Ticket not found")
    return db_ticket


@router.post("/", response_model=TicketResponse, status_code=201)
def create_ticket(ticket: TicketCreate, db: Session = Depends(get_db)):
    """Create a new ticket."""
    tag_ids = ticket.tag_ids or []
    return crud_tickets.create_ticket(db=db, ticket=ticket, tag_ids=tag_ids)


@router.put("/{ticket_id}", response_model=TicketResponse)
def update_ticket(ticket_id: int, ticket_update: TicketUpdate, db: Session = Depends(get_db)):
    """Update a ticket."""
    db_ticket = crud_tickets.update_ticket(db, ticket_id=ticket_id, ticket_update=ticket_update)
    if db_ticket is None:
        raise HTTPException(status_code=404, detail="Ticket not found")
    return db_ticket


@router.patch("/{ticket_id}/complete", response_model=TicketResponse)
def complete_ticket(ticket_id: int, db: Session = Depends(get_db)):
    """Mark a ticket as completed."""
    db_ticket = crud_tickets.complete_ticket(db, ticket_id=ticket_id)
    if db_ticket is None:
        raise HTTPException(status_code=404, detail="Ticket not found")
    return db_ticket


@router.patch("/{ticket_id}/uncomplete", response_model=TicketResponse)
def uncomplete_ticket(ticket_id: int, db: Session = Depends(get_db)):
    """Mark a ticket as pending (uncomplete)."""
    db_ticket = crud_tickets.uncomplete_ticket(db, ticket_id=ticket_id)
    if db_ticket is None:
        raise HTTPException(status_code=404, detail="Ticket not found")
    return db_ticket


@router.delete("/{ticket_id}", status_code=204)
def delete_ticket(ticket_id: int, db: Session = Depends(get_db)):
    """Delete a ticket."""
    success = crud_tickets.delete_ticket(db, ticket_id=ticket_id)
    if not success:
        raise HTTPException(status_code=404, detail="Ticket not found")
    return None


@router.post("/{ticket_id}/tags", response_model=TicketResponse)
def add_tags_to_ticket(
    ticket_id: int,
    request: TagIdsRequest,
    db: Session = Depends(get_db),
):
    """Add tags to a ticket."""
    db_ticket = crud_tickets.add_tags_to_ticket(db, ticket_id=ticket_id, tag_ids=request.tag_ids)
    if db_ticket is None:
        raise HTTPException(status_code=404, detail="Ticket not found")
    return db_ticket


@router.delete("/{ticket_id}/tags/{tag_id}", response_model=TicketResponse)
def remove_tag_from_ticket(ticket_id: int, tag_id: int, db: Session = Depends(get_db)):
    """Remove a tag from a ticket."""
    db_ticket = crud_tickets.remove_tag_from_ticket(db, ticket_id=ticket_id, tag_id=tag_id)
    if db_ticket is None:
        raise HTTPException(status_code=404, detail="Ticket or tag not found")
    return db_ticket
