from fastapi import FastAPI, Query, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from database import get_db, engine
from models import Base, User
from schemas import UserCreate, UserResponse


app = FastAPI()
Base.metadata.create_all(bind=engine)


# health endpoint
@app.get("/health")
def health_check():
    return {"status": "ok"}


@app.post("/users", status_code=201, response_model=UserResponse)
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    """
    Create a new user in the database.

    Flow:
    Client JSON → UserCreate validation → create ORM User →
    db.add() → db.commit() → db.refresh() → return user.

    The database enforces the unique email constraint.
    Duplicate emails raise an IntegrityError which is returned
    as a 409 Conflict response.
    """

    new_user = User(email=user.email)

    try:
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
        return new_user

    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=409, detail="Email already exists")


@app.get("/users/{user_id}")
def get_user(user_id: int):
    return {"user_id": user_id}


@app.get("/notes")
def get_notes(
    page: int = Query(default=1, ge=1), limit: int = Query(default=1, ge=1, le=100)
):
    return {"page": page, "limit": limit}
