from typing import List, Optional
from pydantic import BaseModel
from .note import NoteResponse
from .main_accord import MainAccord
from .brand import Brand
from .type import Type
from .family import Family
from .country import Country
from .concentration import Concentration
from .perfumer import Perfumer

class PerfumeNoteBase(BaseModel):
    note_id: int
    note_type: str  # 'top', 'middle', or 'base'

class PerfumeNote(PerfumeNoteBase):
    note: NoteResponse

    class Config:
        from_attributes = True

class PerfumeBase(BaseModel):
    name: str
    brand_id: int
    concentration_id: Optional[int] = None
    local_image_path: Optional[str] = None
    gender: Optional[str] = None
    type_id: Optional[int] = None
    family_id: Optional[int] = None
    category: Optional[str] = None
    release_year: Optional[int] = None
    country_id: Optional[int] = None
    description: Optional[str] = None
    longevity: Optional[str] = None
    sillage: Optional[str] = None
    occasion: Optional[List[str]] = None
    season: Optional[List[str]] = None
    perfumer_id: Optional[int] = None
    inspiration: Optional[str] = None
    istrend: Optional[dict] = None

class PerfumeCreate(PerfumeBase):
    notes: Optional[List[PerfumeNoteBase]] = None
    main_accord_ids: Optional[List[int]] = None

class PerfumeUpdate(PerfumeBase):
    name: Optional[str] = None
    brand_id: Optional[int] = None
    notes: Optional[List[PerfumeNoteBase]] = None
    main_accord_ids: Optional[List[int]] = None

class Perfume(PerfumeBase):
    id: int
    brand: Brand
    concentration: Optional[Concentration] = None
    type: Optional[Type] = None
    family: Optional[Family] = None
    country: Optional[Country] = None
    perfumer: Optional[Perfumer] = None
    notes: List[PerfumeNote] = []
    main_accords: List[MainAccord] = []

    class Config:
        from_attributes = True 