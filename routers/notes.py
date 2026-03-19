from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from database import get_db
from schemas.note import NoteCreate, NoteResponse
from services import note_service
from exceptions import NoteNotFoundError,UserNotFoundError

router = APIRouter(prefix="/notes", tags=["Notes"])


@router.post("/", status_code=201, response_model=NoteResponse)
def create_note(note_data: NoteCreate, db: Session = Depends(get_db)):
    """
    Create a new note.

    - Pydantic validates request body before this runs
    - Service checks if owner exists first → 404 if not
    - owner_id links note to a user (foreign key → users.id)
    """
    try:
        return note_service.create_note(
            db, note_data.title, note_data.content, note_data.owner_id
        )
    except UserNotFoundError:
        raise HTTPException(status_code=404, detail="User not found")


@router.get("/", response_model=list[NoteResponse])
def list_notes(
    page: int = Query(1, ge=1),
    limit: int = Query(10, ge=1, le=100),
    db: Session = Depends(get_db),
):
    """
    Return paginated list of all notes.

    - page starts at 1, limit max is 100
    - ordering and offset handled in service
    """
    return note_service.list_notes(db, page, limit)


@router.get("/{note_id}", response_model=NoteResponse)
def get_note(note_id: int, db: Session = Depends(get_db)):
    """
    Fetch a single note by ID.

    - note_id comes from URL path e.g. /notes/3
    - Service raises NoteNotFoundError if missing → 404
    """
    try:
        return note_service.get_note_by_id(db, note_id)
    except NoteNotFoundError:
        raise HTTPException(status_code=404, detail="Note not found")


@router.get("/user/{user_id}", response_model=list[NoteResponse])
def get_notes_by_user(
    user_id: int,
    page: int = Query(1, ge=1),
    limit: int = Query(10, ge=1, le=100),
    db: Session = Depends(get_db),
):
    return note_service.get_notes_by_user(db, user_id, page, limit)
