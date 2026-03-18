from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from database import get_db
from models import User
from datetime import datetime

router = APIRouter(prefix="/users", tags=["Users"])

# ------------------------------
# CREATE USER
# ------------------------------
@router.post("/", status_code=201)
def create_user(email: str, db: Session = Depends(get_db)):
    """
    Create a new user.

    Flow:
        1. Validate input (email)
        2. Check if email already exists
        3. Create User ORM object
        4. Add to DB session
        5. Commit & refresh
        6. Return created user
    """
    existing_user = db.query(User).filter(User.email == email).first()
    if existing_user:
        raise HTTPException(status_code=409, detail="Email already exists")

    new_user = User(email=email)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


# ------------------------------
# LIST USERS (PAGINATED)
# ------------------------------
@router.get("/")
def list_users(
    page: int = Query(1, ge=1),
    limit: int = Query(10, ge=1, le=100),
    db: Session = Depends(get_db),
):
    """
    Return a paginated list of users.
    """
    offset = (page - 1) * limit
    users = db.query(User).order_by(User.id).offset(offset).limit(limit).all()
    return users


# ------------------------------
# GET SINGLE USER
# ------------------------------
@router.get("/{user_id}")
def get_user(user_id: int, db: Session = Depends(get_db)):
    """
    Fetch a single user by ID.
    """
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user