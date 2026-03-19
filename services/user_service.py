from sqlalchemy.orm import Session
from models import User
from exceptions import DuplicateEmailError, UserNotFoundError


def create_user(db: Session, email: str) -> User:
    """
    Insert a new user into the DB.

    - Checks if email already exists first
    - If duplicate → raises DuplicateEmailError (router catches → 409)
    - If clean → creates user, commits, refreshes and returns the new object
    - db.refresh() re-fetches the row so we get DB-generated fields
      like id and created_at back on the object
    """
    existing = db.query(User).filter(User.email == email).first()
    if existing:
        raise DuplicateEmailError(f"Email already exists: {email}")

    new_user = User(email=email)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


def get_user_by_id(db: Session, user_id: int) -> User:
    """
    Fetch a single user by their ID.

    - Translates to: SELECT * FROM users WHERE id = user_id LIMIT 1
    - If not found → raises UserNotFoundError (router catches → 404)
    - Always returns a User — never returns None
    """
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise UserNotFoundError(f"User with id {user_id} not found")
    return user


def list_users(db: Session, page: int, limit: int) -> list[User]:
    """
    Fetch a paginated list of users ordered by ID.

    - offset is calculated here so the router doesn't think about it
    - Translates to: SELECT * FROM users ORDER BY id LIMIT limit OFFSET offset
    - Returns empty list if no users found — not an error
    """
    offset = (page - 1) * limit
    return db.query(User).order_by(User.id).offset(offset).limit(limit).all()
