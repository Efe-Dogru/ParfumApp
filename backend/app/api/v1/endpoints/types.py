from typing import List
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.db.session import get_db
from app.models.type import Type as TypeModel
from app.schemas.type import Type

router = APIRouter()

@router.get("/", response_model=List[Type])
async def read_types(
    db: AsyncSession = Depends(get_db),
    skip: int = 0,
    limit: int = 100
):
    """
    Retrieve types.
    """
    query = select(TypeModel).offset(skip).limit(limit)
    result = await db.execute(query)
    types = result.scalars().all()
    return types 