from pydantic import BaseModel

class MainAccord(BaseModel):
    id: int
    name: str

    class Config:
        from_attributes = True 