from pydantic import BaseModel

class NoteBase(BaseModel):
    name: str

class NoteCreate(NoteBase):
    pass

class Note(NoteBase):
    id: int

    class Config:
        from_attributes = True

# Specific note types using the same base structure
class TopNote(Note):
    pass

class MiddleNote(Note):
    pass

class BaseNote(Note):
    pass 