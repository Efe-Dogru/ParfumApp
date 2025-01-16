from pydantic import BaseModel
from typing import Optional, List

class PerfumeBase(BaseModel):
    name: str
    brand: str
    type: Optional[str] = None
    gender: Optional[str] = None
    family: Optional[str] = None
    release_year: Optional[int] = None
    concentration: Optional[str] = None
    description: Optional[str] = None
    longevity: Optional[str] = None
    sillage: Optional[str] = None
    image_url: Optional[str] = None
    perfumer: Optional[str] = None
    inspiration: Optional[str] = None

class PerfumeCreate(PerfumeBase):
    top_note_ids: Optional[List[int]] = None
    middle_note_ids: Optional[List[int]] = None
    base_note_ids: Optional[List[int]] = None
    main_accord_ids: Optional[List[int]] = None
    occasion_ids: Optional[List[int]] = None
    season_ids: Optional[List[int]] = None

class PerfumeUpdate(PerfumeBase):
    name: Optional[str] = None
    brand: Optional[str] = None
    top_note_ids: Optional[List[int]] = None
    middle_note_ids: Optional[List[int]] = None
    base_note_ids: Optional[List[int]] = None
    main_accord_ids: Optional[List[int]] = None
    occasion_ids: Optional[List[int]] = None
    season_ids: Optional[List[int]] = None

class NoteBase(BaseModel):
    id: int
    name: str

    class Config:
        from_attributes = True

class MainAccordBase(BaseModel):
    id: int
    name: str

    class Config:
        from_attributes = True

class OccasionBase(BaseModel):
    id: int
    name: str

    class Config:
        from_attributes = True

class SeasonBase(BaseModel):
    id: int
    name: str

    class Config:
        from_attributes = True

class Perfume(PerfumeBase):
    id: int
    top_notes: List[NoteBase] = []
    middle_notes: List[NoteBase] = []
    base_notes: List[NoteBase] = []
    main_accords: List[MainAccordBase] = []
    occasions: List[OccasionBase] = []
    seasons: List[SeasonBase] = []

    class Config:
        from_attributes = True 