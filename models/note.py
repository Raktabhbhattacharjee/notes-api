from datetime import datetime, timezone
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from .base import Base  # relative import to the Base class

class Note(Base):
    __tablename__ = "notes"

    # Primary key
    id = Column(Integer, primary_key=True)

    # Note fields
    title = Column(String, nullable=False)
    content = Column(String, nullable=False)

    # Timestamp
    created_at = Column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        nullable=False,
    )

    # Foreign key to User
    owner_id = Column(Integer, ForeignKey("users.id"), nullable=False)

    # Relationship to User (back_populates must match User.notes)
    owner = relationship("User", back_populates="notes")