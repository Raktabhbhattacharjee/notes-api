from datetime import datetime
from pydantic import BaseModel, ConfigDict

class NoteCreate(BaseModel):
    title: str
    content: str
    owner_id: int  # client sends owner ID

class NoteResponse(BaseModel):
    id: int
    title: str
    content: str
    created_at: datetime
    owner_id: int
    model_config = ConfigDict(from_attributes=True)
    



class PaginatedNotes(BaseModel):
    items: list[NoteResponse]
    total: int
    page: int
    has_next: bool
    has_prev: bool