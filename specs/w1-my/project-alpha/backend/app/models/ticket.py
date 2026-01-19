"""Ticket model."""
import enum
from sqlalchemy import Column, Integer, String, Text, DateTime, Enum, CheckConstraint
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.database import Base


class TicketStatus(str, enum.Enum):
    """Ticket status enumeration."""

    PENDING = "pending"
    COMPLETED = "completed"


class Ticket(Base):
    """Ticket model."""

    __tablename__ = "tickets"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255), nullable=False)
    description = Column(Text)
    status = Column(
        Enum(TicketStatus, native_enum=False, values_callable=lambda x: [e.value for e in x]),
        default=TicketStatus.PENDING.value,
        nullable=False,
    )
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    completed_at = Column(DateTime(timezone=True), nullable=True)

    # Relationship with tags
    tags = relationship("Tag", secondary="ticket_tags", back_populates="tickets")

    __table_args__ = (
        CheckConstraint("status IN ('pending', 'completed')", name="check_status"),
    )
