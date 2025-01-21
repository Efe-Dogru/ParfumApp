from pydantic import BaseModel

class FamilyBase(BaseModel):
    name: str

class FamilyCreate(FamilyBase):
    pass

class Family(FamilyBase):
    id: int

    class Config:
        from_attributes = True 