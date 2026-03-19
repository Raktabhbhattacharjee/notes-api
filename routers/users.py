from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from database import get_db
from schemas.user import UserCreate, UserResponse
from services import user_service
from exceptions import DuplicateEmailError,UserNotFoundError

router = APIRouter(prefix="/users", tags=["Users"])


# ------------------------------
# CREATE USER
# ------------------------------
@router.post("/", status_code=201, response_model=UserResponse)
def create_user(user_data: UserCreate, db: Session = Depends(get_db)):
    """
    Create a new user.

    - Pydantic validates the email format before this even runs
    - Service checks if email already exists in DB
    - If duplicate → 409 Conflict
    - If all good → user gets created and returned
    """
    
    try:
        return user_service.create_user(db,user_data.email)
    except DuplicateEmailError:
        raise HTTPException(status_code=409,detail="Email already exists")

# ------------------------------
# LIST USERS (PAGINATED)
# ------------------------------
@router.get("/", response_model=list[UserResponse])
def list_users(
    page: int = Query(1, ge=1),
    limit: int = Query(10, ge=1, le=100),
    db: Session = Depends(get_db),
):
    """
    Return a paginated list of users.

    - page: which page you want (starts at 1)
    - limit: how many users per page (max 100)
    - offset is calculated in the service (page - 1) * limit
    - ordered by user ID so results are consistent
    """
    return user_service.list_users(db, page, limit)


# ------------------------------
# GET SINGLE USER
# ------------------------------
@router.get("/{user_id}", response_model=UserResponse)
def get_user(user_id: int, db: Session = Depends(get_db)):
    """
    Fetch a single user by their ID.

    - user_id comes from the URL path (e.g. /users/3)
    - If user doesn't exist → 404 Not Found
    - If found → returns user data
    """
    try:
        return user_service.get_user_by_id(db,user_id)
    except UserNotFoundError:
        raise HTTPException(status_code=404,detail="User not found")
    