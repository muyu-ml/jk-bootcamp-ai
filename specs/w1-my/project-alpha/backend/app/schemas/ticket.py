"""Ticket Pydantic schemas."""
from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional, List
from app.schemas.tag import TagResponse


class TicketBase(BaseModel):
    """Base ticket schema."""

    title: str = Field(..., min_length=1, max_length=255)
    description: Optional[str] = Field(None, max_length=10000)


class TicketCreate(TicketBase):
    """Schema for creating a ticket."""

    tag_ids: Optional[List[int]] = Field(default_factory=list)


class TicketUpdate(BaseModel):
    """Schema for updating a ticket."""

    title: Optional[str] = Field(None, min_length=1, max_length=255)
    description: Optional[str] = Field(None, max_length=10000)


class TicketResponse(TicketBase):
    """Schema for ticket response."""

    id: int
    status: str
    tags: List["TagResponse"] = Field(default_factory=list)
    created_at: datetime
    updated_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None

    class Config:
        from_attributes = True


class TicketListResponse(BaseModel):
    """Schema for paginated ticket list response."""

    tickets: List[TicketResponse]
    total: int
    limit: Optional[int] = None
    offset: int = 0
