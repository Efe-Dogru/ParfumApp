from pydantic import BaseModel, Field

class OccasionBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)

class OccasionCreate(OccasionBase):
    pass

class OccasionResponse(OccasionBase):
    id: int

    class Config:
        from_attributes = True 