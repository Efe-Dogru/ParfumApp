from pydantic import BaseModel

class CountryBase(BaseModel):
    name: str

class CountryCreate(CountryBase):
    pass

class Country(CountryBase):
    id: int

    class Config:
        from_attributes = True 