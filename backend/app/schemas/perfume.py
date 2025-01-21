from typing import List, Optional
from pydantic import BaseModel
from .note import TopNote, MiddleNote, BaseNote
from .main_accord import MainAccord
from .brand import Brand
from .type import Type
from .family import Family
from .country import Country
from .concentration import Concentration
from .perfumer import Perfumer

class PerfumeBase(BaseModel):
    name: str
    brand_id: int
    concentration_id: Optional[int] = None
    local_image_path: Optional[str] = None
    gender: Optional[str] = None
    type_id: Optional[int] = None
    family_id: Optional[int] = None
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
    top_note_ids: Optional[List[int]] = None
    middle_note_ids: Optional[List[int]] = None
    base_note_ids: Optional[List[int]] = None
    main_accord_ids: Optional[List[int]] = None

class PerfumeUpdate(PerfumeBase):
    name: Optional[str] = None
    brand_id: Optional[int] = None
    top_note_ids: Optional[List[int]] = None
    middle_note_ids: Optional[List[int]] = None
    base_note_ids: Optional[List[int]] = None
    main_accord_ids: Optional[List[int]] = None

class Perfume(PerfumeBase):
    id: int
    brand: Brand
    concentration: Optional[Concentration] = None
    type: Optional[Type] = None
    family: Optional[Family] = None
    country: Optional[Country] = None
    perfumer: Optional[Perfumer] = None
    top_notes: List[TopNote] = []
    middle_notes: List[MiddleNote] = []
    base_notes: List[BaseNote] = []
    main_accords: List[MainAccord] = []

    class Config:
        from_attributes = True 