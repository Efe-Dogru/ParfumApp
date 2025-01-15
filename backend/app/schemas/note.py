from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel, Field
from app.models.note import NoteType

# Shared properties
class NoteBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)
    description: Optional[str] = Field(None, max_length=500)
    category: Optional[str] = Field(None, max_length=100)

# Properties to receive on note creation
class NoteCreate(NoteBase):
    pass

# Properties to receive on note update
class NoteUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=1, max_length=100)
    description: Optional[str] = Field(None, max_length=500)
    category: Optional[str] = Field(None, max_length=100)

# Properties shared by models stored in DB
class NoteInDBBase(NoteBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

# Properties to return to client
class NoteResponse(NoteInDBBase):
    pass

# Schema for adding a note to a perfume
class PerfumeNoteCreate(BaseModel):
    note_id: int
    note_type: NoteType 