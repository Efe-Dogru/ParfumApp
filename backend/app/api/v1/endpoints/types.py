from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.db.session import get_db
from app.models.type import Type as TypeModel
from app.schemas.type import Type, TypeCreate

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

@router.post("/", response_model=Type)
async def create_type(
    *,
    db: AsyncSession = Depends(get_db),
    type_in: TypeCreate
):
    """
    Create new type.
    """
    query = select(TypeModel).filter(TypeModel.name == type_in.name)
    result = await db.execute(query)
    db_type = result.scalar_one_or_none()
    
    if db_type:
        raise HTTPException(
            status_code=400,
            detail="Type with this name already exists."
        )
    
    db_type = TypeModel(name=type_in.name)
    db.add(db_type)
    await db.commit()
    await db.refresh(db_type)
    return db_type

@router.get("/{type_id}", response_model=Type)
async def read_type(
    *,
    db: AsyncSession = Depends(get_db),
    type_id: int
):
    """
    Get type by ID.
    """
    query = select(TypeModel).filter(TypeModel.id == type_id)
    result = await db.execute(query)
    type_obj = result.scalar_one_or_none()
    
    if not type_obj:
        raise HTTPException(
            status_code=404,
            detail="Type not found"
        )
    return type_obj 