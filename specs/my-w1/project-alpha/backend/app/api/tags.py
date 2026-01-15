"""Tag API routes."""
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional

from app.database import get_db
from app.schemas.tag import TagCreate, TagUpdate, TagResponse
from app.crud import tags as crud_tags

router = APIRouter()


@router.get("/", response_model=List[TagResponse])
def get_tags(
    skip: int = Query(0, ge=0, description="Number of results to skip"),
    limit: int = Query(100, ge=1, le=1000, description="Maximum number of results"),
    db: Session = Depends(get_db),
):
    """Get all tags."""
    db_tags = crud_tags.get_tags(db, skip=skip, limit=limit)
    # Add ticket_count to each tag using optimized query
    result = []
    for tag in db_tags:
        ticket_count = crud_tags.get_tag_ticket_count(db, tag.id)
        tag_dict = {
            "id": tag.id,
            "name": tag.name,
            "color": tag.color,
            "created_at": tag.created_at,
            "ticket_count": ticket_count,
        }
        result.append(TagResponse(**tag_dict))
    return result


@router.get("/{tag_id}", response_model=TagResponse)
def get_tag(tag_id: int, db: Session = Depends(get_db)):
    """Get a tag by ID."""
    db_tag = crud_tags.get_tag(db, tag_id=tag_id)
    if db_tag is None:
        raise HTTPException(status_code=404, detail="Tag not found")
    ticket_count = crud_tags.get_tag_ticket_count(db, tag_id)
    tag_dict = {
        "id": db_tag.id,
        "name": db_tag.name,
        "color": db_tag.color,
        "created_at": db_tag.created_at,
        "ticket_count": ticket_count,
    }
    return TagResponse(**tag_dict)


@router.post("/", response_model=TagResponse, status_code=201)
def create_tag(tag: TagCreate, db: Session = Depends(get_db)):
    """Create a new tag."""
    # Check if tag with same name already exists
    existing_tag = crud_tags.get_tag_by_name(db, name=tag.name)
    if existing_tag:
        raise HTTPException(status_code=400, detail="Tag with this name already exists")
    return crud_tags.create_tag(db=db, tag=tag)


@router.put("/{tag_id}", response_model=TagResponse)
def update_tag(tag_id: int, tag_update: TagUpdate, db: Session = Depends(get_db)):
    """Update a tag."""
    # Check if name is being changed and if it conflicts with existing tag
    if tag_update.name:
        existing_tag = crud_tags.get_tag_by_name(db, name=tag_update.name)
        if existing_tag and existing_tag.id != tag_id:
            raise HTTPException(status_code=400, detail="Tag with this name already exists")

    db_tag = crud_tags.update_tag(db, tag_id=tag_id, tag_update=tag_update)
    if db_tag is None:
        raise HTTPException(status_code=404, detail="Tag not found")
    ticket_count = crud_tags.get_tag_ticket_count(db, tag_id)
    tag_dict = {
        "id": db_tag.id,
        "name": db_tag.name,
        "color": db_tag.color,
        "created_at": db_tag.created_at,
        "ticket_count": ticket_count,
    }
    return TagResponse(**tag_dict)


@router.delete("/{tag_id}", status_code=204)
def delete_tag(tag_id: int, db: Session = Depends(get_db)):
    """Delete a tag."""
    success = crud_tags.delete_tag(db, tag_id=tag_id)
    if not success:
        raise HTTPException(status_code=404, detail="Tag not found")
    return None
