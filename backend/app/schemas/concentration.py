from pydantic import BaseModel

class ConcentrationBase(BaseModel):
    name: str

class ConcentrationCreate(ConcentrationBase):
    pass

class Concentration(ConcentrationBase):
    id: int

    class Config:
        from_attributes = True 