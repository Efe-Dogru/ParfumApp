from typing import List, Optional
from pydantic import BaseModel
from .note import Note
from .main_accord import MainAccord
from .brand import Brand
from .type import Type
from .family import Family
from .country import Country
from .concentration import Concentration
from .perfumer import Perfumer

class Tag(BaseModel):
    id: int
    name: str

    class Config:
        from_attributes = True

class PerfumeNote(BaseModel):
    note_type: str  # 'top', 'middle', or 'base'
    note: str

    class Config:
        from_attributes = True

class Perfume(BaseModel):
    id: int
    name: str
    local_image_path: Optional[str] = None
    gender: Optional[str] = None
    category: Optional[str] = None
    release_year: Optional[int] = None
    description: Optional[str] = None
    longevity: Optional[str] = None
    sillage: Optional[str] = None
    occasion: Optional[List[str]] = None
    season: Optional[List[str]] = None
    inspiration: Optional[str] = None
    brand: str
    concentration: Optional[str] = None
    type: Optional[str] = None
    family: Optional[str] = None
    country: Optional[str] = None
    perfumer: Optional[str] = None
    perfume_notes: List[PerfumeNote] = []
    main_accords: List[str] = []
    tags: List[str] = []

    class Config:
        from_attributes = True

class PerfumeList(BaseModel):
    id: int
    name: str
    brand_name: str
    local_image_path: Optional[str] = None

    class Config:
        from_attributes = True 