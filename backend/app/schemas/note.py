from typing import Optional, List
from pydantic import BaseModel

class NoteFamily(BaseModel):
    id: int
    name: str

    class Config:
        from_attributes = True

class NoteMood(BaseModel):
    id: int
    name: str

    class Config:
        from_attributes = True

class Note(BaseModel):
    id: int
    name: str
    normalized_name: str
    image_filename: Optional[str] = None
    description: Optional[str] = None
    source: Optional[str] = None
    cultural_significance: Optional[str] = None
    family_id: Optional[int] = None
    family: Optional[NoteFamily] = None
    moods: List[NoteMood] = []

    class Config:
        from_attributes = True

class NoteList(BaseModel):
    id: int
    name: str
    image_filename: Optional[str] = None

    class Config:
        from_attributes = True 