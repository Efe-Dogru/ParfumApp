from pydantic import BaseModel

class PerfumerBase(BaseModel):
    name: str

class PerfumerCreate(PerfumerBase):
    pass

class Perfumer(PerfumerBase):
    id: int

    class Config:
        from_attributes = True 