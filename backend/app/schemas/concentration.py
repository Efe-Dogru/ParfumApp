from pydantic import BaseModel

class Concentration(BaseModel):
    id: int
    name: str

    class Config:
        from_attributes = True 