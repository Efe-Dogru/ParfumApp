from pydantic import BaseModel

class Perfumer(BaseModel):
    id: int
    name: str

    class Config:
        from_attributes = True 