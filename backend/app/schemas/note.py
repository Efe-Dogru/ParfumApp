from typing import Optional
from pydantic import BaseModel

class NoteBase(BaseModel):
    name: str
    image_filename: Optional[str] = None

class NoteCreate(NoteBase):
    pass

class NoteResponse(NoteBase):
    id: int
    normalized_name: str

    class Config:
        from_attributes = True 