from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from database import get_db
from models import Note, User
from datetime import datetime

router = APIRouter(prefix="/notes", tags=["Notes"])

# ------------------------------
# CREATE NOTE
# ------------------------------
@router.post("/", status_code=201)
def create_note(title: str, content: str, owner_id: int, db: Session = Depends(get_db)):
    """
    Create a new note for a given user.
    """
    # Check if user exists
    user = db.query(User).filter(User.id == owner_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    new_note = Note(title=title, content=content, owner_id=owner_id)
    db.add(new_note)
    db.commit()
    db.refresh(new_note)
    return new_note


# ------------------------------
# LIST NOTES (PAGINATED)
# ------------------------------
@router.get("/")
def list_notes(
    page: int = Query(1, ge=1),
    limit: int = Query(10, ge=1, le=100),
    db: Session = Depends(get_db),
):
    """
    Return paginated list of notes.
    """
    offset = (page - 1) * limit
    notes = db.query(Note).order_by(Note.id).offset(offset).limit(limit).all()
    return notes


# ------------------------------
# GET SINGLE NOTE
# ------------------------------
@router.get("/{note_id}")
def get_note(note_id: int, db: Session = Depends(get_db)):
    """
    Fetch a single note by ID.
    """
    note = db.query(Note).filter(Note.id == note_id).first()
    if not note:
        raise HTTPException(status_code=404, detail="Note not found")
    return note


# ------------------------------
# GET NOTES FOR SPECIFIC USER
# ------------------------------
@router.get("/user/{user_id}")
def get_user_notes(
    user_id: int,
    page: int = Query(1, ge=1),
    limit: int = Query(10, ge=1, le=100),
    db: Session = Depends(get_db),
):
    """
    Return a paginated list of notes belonging to a specific user.
    """
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    offset = (page - 1) * limit
    notes = (
        db.query(Note)
        .filter(Note.owner_id == user_id)
        .order_by(Note.id)
        .offset(offset)
        .limit(limit)
        .all()
    )
    return notes


# ------------------------------
# DELETE NOTE
# ------------------------------
@router.delete("/{note_id}", status_code=204)
def delete_note(note_id: int, db: Session = Depends(get_db)):
    """
    Delete a note by ID.
    """
    note = db.query(Note).filter(Note.id == note_id).first()
    if not note:
        raise HTTPException(status_code=404, detail="Note not found")

    db.delete(note)
    db.commit()
    return