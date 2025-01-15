from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class PerfumeBase(BaseModel):
    brand: str
    brand_line: Optional[str] = None
    name: str
    image_url: Optional[str] = None
    geurnoot: Optional[str] = None
    topnoot: Optional[str] = None
    hartnoot: Optional[str] = None
    basisnoot: Optional[str] = None

class PerfumeCreate(PerfumeBase):
    pass

class PerfumeUpdate(PerfumeBase):
    pass

class Perfume(PerfumeBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True 