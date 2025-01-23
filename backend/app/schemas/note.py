from typing import Optional
from pydantic import BaseModel

class NoteBase(BaseModel):
    name: str
    image_filename: Optional[str] = None
    description: Optional[str] = None
    family: Optional[str] = None
    source: Optional[str] = None
    cultural_significance: Optional[str] = None
    mood: Optional[str] = None

class NoteCreate(NoteBase):
    pass

class NoteResponse(NoteBase):
    id: int
    normalized_name: str

    class Config:
        from_attributes = True 