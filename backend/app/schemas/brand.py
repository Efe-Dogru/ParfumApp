from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel, Field, HttpUrl

# Shared properties
class BrandBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)
    description: Optional[str] = Field(None, max_length=1000)
    founded_year: Optional[int] = None
    country: Optional[str] = Field(None, max_length=100)
    website: Optional[HttpUrl] = None

# Properties to receive on brand creation
class BrandCreate(BrandBase):
    pass

# Properties to receive on brand update
class BrandUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=1, max_length=100)
    description: Optional[str] = Field(None, max_length=1000)
    founded_year: Optional[int] = None
    country: Optional[str] = Field(None, max_length=100)
    website: Optional[HttpUrl] = None

# Properties shared by models stored in DB
class BrandInDBBase(BrandBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

# Properties to return to client
class BrandResponse(BrandInDBBase):
    pass 