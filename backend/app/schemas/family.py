from pydantic import BaseModel

class Family(BaseModel):
    id: int
    name: str

    class Config:
        from_attributes = True 