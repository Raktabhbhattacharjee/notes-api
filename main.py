# -------------------------------------------------------------
# NOTE TO SELF
#
# `User` and `user` are NOT the same thing.
#
# User → SQLAlchemy ORM model (represents the "users" table)
# user → Pydantic request object containing client input
#
# Example:
# user.email → email sent in the request body
# User.id    → id column from the database table
#
# Creating a DB row:
# new_user = User(email=user.email)
# -------------------------------------------------------------

from fastapi import FastAPI, Query, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

from database import get_db, engine
from models import Base, User, Note
from schemas import UserCreate, UserResponse,NoteCreate,NoteResponse


# -------------------------------------------------------------
# FastAPI application instance
# -------------------------------------------------------------
app = FastAPI()


# -------------------------------------------------------------
# Create database tables automatically (development only)
#
# SQLAlchemy inspects ORM models and generates tables if missing.
# In production this is usually replaced by migration tools
# like Alembic.
# -------------------------------------------------------------
Base.metadata.create_all(bind=engine)


# =============================================================
# CREATE USER
# =============================================================
@app.post("/users", status_code=201, response_model=UserResponse)
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    """
    Create a new user.

    Request Flow:
        Client JSON
        ↓
        Pydantic validation (UserCreate)
        ↓
        Convert request data → ORM object
        ↓
        Add to database session
        ↓
        Commit transaction
        ↓
        Refresh ORM instance
        ↓
        Return response model

    Why refresh?
        After commit, the database generates values
        like `id` or `created_at`. `db.refresh()` loads
        those values back into the ORM object.

    Error Handling:
        The database enforces the UNIQUE constraint
        on email. If a duplicate email is inserted,
        PostgreSQL raises an IntegrityError.

        We catch it and return HTTP 409 Conflict.
    """

    # Create ORM object from validated request data
    new_user = User(email=user.email)

    try:
        # Stage the object in the session
        db.add(new_user)

        # Persist the transaction to the database
        db.commit()

        # Reload DB-generated values (like id)
        db.refresh(new_user)

        return new_user

    except IntegrityError:
        # If DB constraint fails, rollback transaction
        db.rollback()

        raise HTTPException(
            status_code=409,
            detail="Email already exists"
        )


# =============================================================
# LIST USERS (PAGINATED)
# =============================================================
@app.get("/users", response_model=list[UserResponse])
def list_users(
    page: int = Query(default=1, ge=1),
    limit: int = Query(default=10, ge=1, le=100),
    db: Session = Depends(get_db),
):
    """
    Return a paginated list of users.

    Query Parameters:
        page  → which page of data to fetch
        limit → how many users per page

    Pagination Logic:
        offset = (page - 1) * limit

    Database Query Pattern:
        ORDER BY → ensures stable pagination
        OFFSET   → skip rows
        LIMIT    → return number of rows

    Example:

        page=1 limit=2
        → OFFSET 0 LIMIT 2
        → returns rows 1,2

        page=2 limit=2
        → OFFSET 2 LIMIT 2
        → returns rows 3,4

    Why return [] instead of 404?
        Because the resource `/users` exists.
        That page simply has no results.
    """

    # Calculate how many rows to skip
    offset = (page - 1) * limit

    # Query database with pagination
    users = (
        db.query(User)
        .order_by(User.id)   # stable ordering
        .offset(offset)      # skip rows
        .limit(limit)        # number of rows to return
        .all()
    )

    return users


# =============================================================
# GET SINGLE USER
# =============================================================
@app.get("/users/{user_id}", response_model=UserResponse)
def get_user(user_id: int, db: Session = Depends(get_db)):
    """
    Fetch a single user by ID.

    Flow:
        Client sends user_id in URL
        ↓
        Query database
        ↓
        If user exists → return user
        If user missing → return 404

    Query Pattern:
        db.query(User)
        .filter(User.id == user_id)
        .first()

    `.first()` returns:
        - the first matching row
        - or None if nothing exists
    """

    # Query database for the user
    user = db.query(User).filter(User.id == user_id).first()

    # Handle case where user does not exist
    if user is None:
        raise HTTPException(
            status_code=404,
            detail="User not found"
        )

    return user

@app.post("/notes", response_model=NoteResponse, status_code=201)
def create_note(note: NoteCreate, db: Session = Depends(get_db)):
    """
    Create a new note.

    Flow:
        Client sends note data
        ↓
        Pydantic validates request body (NoteCreate)
        ↓
        Check if the owner user exists
        ↓
        Create ORM Note object
        ↓
        Add object to DB session
        ↓
        Commit transaction
        ↓
        Refresh ORM instance
        ↓
        Return created note

    Why check user first?
        The `notes.owner_id` column has a foreign key constraint
        referencing `users.id`.

        Instead of letting the database throw a constraint error,
        we check the user explicitly and return a clear API error.

    Error Handling:
        If something unexpected happens during commit,
        the transaction is rolled back and the API returns
        a 500 error.
    """

    user = db.query(User).filter(User.id == note.owner_id).first()

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    new_note = Note(
        title=note.title,
        content=note.content,
        owner_id=note.owner_id
    )

    try:
        db.add(new_note)
        db.commit()
        db.refresh(new_note)
        return new_note

    except Exception:
        db.rollback()
        raise HTTPException(
            status_code=500,
            detail="Could not create note"
        )