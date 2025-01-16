from pydantic import BaseModel, Field

class MainAccordBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)

class MainAccordCreate(MainAccordBase):
    pass

class MainAccordResponse(MainAccordBase):
    id: int

    class Config:
        from_attributes = True 