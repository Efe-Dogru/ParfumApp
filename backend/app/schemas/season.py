from pydantic import BaseModel, Field

class SeasonBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=50)

class SeasonCreate(SeasonBase):
    pass

class SeasonResponse(SeasonBase):
    id: int

    class Config:
        from_attributes = True 