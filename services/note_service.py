from sqlalchemy.orm import Session
from models import Note, User
from exceptions import NoteNotFoundError, UserNotFoundError


def create_note(db: Session, title: str, content: str, owner_id: int) -> Note:
    """
    INSERT INTO notes (title, content, owner_id) VALUES (:title, :content, :owner_id)
    RETURNING *;

    - First checks if owner exists (SELECT * FROM users WHERE id = owner_id)
    - If user not found → raises UserNotFoundError (router catches → 404)
    - owner_id is the foreign key → links to users.id
    - db.refresh() gets the DB generated fields back (id, created_at)
    """
    user = db.query(User).filter(User.id == owner_id).first()
    if not user:
        raise UserNotFoundError(f"User with id {owner_id} not found")

    note = Note(title=title, content=content, owner_id=owner_id)
    db.add(note)
    db.commit()
    db.refresh(note)
    return note


def get_note_by_id(db: Session, note_id: int) -> Note:
    """
    SELECT * FROM notes WHERE id = :note_id LIMIT 1;

    - If no rows returned → raises NoteNotFoundError (router catches → 404)
    - Always returns a Note — never returns None
    """
    note = db.query(Note).filter(Note.id == note_id).first()
    if not note:
        raise NoteNotFoundError(f"Note with id {note_id} not found")
    return note


def list_notes(db: Session, page: int, limit: int, search: str | None = None) -> list[Note]:
    """
    SELECT * FROM notes
    WHERE title ILIKE '%search%'   -- only if search param is provided
    ORDER BY id
    LIMIT :limit OFFSET :offset;

    - search is optional -- if not passed, returns all notes
    - ILIKE means case insensitive, so 'quantum' matches 'Quantum Notes'
    - offset = (page - 1) * limit calculated here
    - query is built step by step -- filter only added if search exists
    - Returns empty list if no rows -- not an error
    """
    offset = (page - 1) * limit
    query = db.query(Note)

    if search:
        query = query.filter(Note.title.ilike(f"%{search}%"))

    return query.order_by(Note.id).offset(offset).limit(limit).all()


def get_notes_by_user(db: Session, user_id: int, page: int, limit: int) -> list[Note]:
    """
    SELECT * FROM notes
    WHERE owner_id = :user_id
    ORDER BY id
    LIMIT :limit OFFSET :offset;

    - owner_id is the join condition between notes and users
    - Returns empty list if user has no notes — not an error
    """
    offset = (page - 1) * limit
    return (
        db.query(Note)
        .filter(Note.owner_id == user_id)
        .order_by(Note.id)
        .offset(offset)
        .limit(limit)
        .all()
    )
