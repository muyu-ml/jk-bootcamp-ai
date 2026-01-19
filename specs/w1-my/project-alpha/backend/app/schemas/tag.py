"""Tag Pydantic schemas."""
from pydantic import BaseModel, Field, field_validator
from datetime import datetime
from typing import Optional
import re


class TagBase(BaseModel):
    """Base tag schema."""

    name: str = Field(..., min_length=1, max_length=50)
    color: Optional[str] = Field(None, pattern="^#[0-9A-Fa-f]{6}$")

    @field_validator("color")
    @classmethod
    def validate_color(cls, v):
        """Validate color format."""
        if v is not None and not re.match(r"^#[0-9A-Fa-f]{6}$", v):
            raise ValueError("Color must be in hex format (#RRGGBB)")
        return v


class TagCreate(TagBase):
    """Schema for creating a tag."""

    pass


class TagUpdate(TagBase):
    """Schema for updating a tag."""

    pass


class TagResponse(TagBase):
    """Schema for tag response."""

    id: int
    created_at: datetime
    ticket_count: Optional[int] = 0

    class Config:
        from_attributes = True
