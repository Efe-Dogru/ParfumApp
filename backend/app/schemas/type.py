from pydantic import BaseModel

class Type(BaseModel):
    id: int
    name: str

    class Config:
        from_attributes = True 