from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.db.session import get_db
from app.models.main_accord import MainAccord as MainAccordModel
from app.schemas.main_accord import MainAccord, MainAccordCreate

router = APIRouter()

@router.get("/", response_model=List[MainAccord])
async def read_main_accords(
    db: AsyncSession = Depends(get_db),
    skip: int = 0,
    limit: int = 100
):
    """
    Retrieve main accords.
    """
    query = select(MainAccordModel).offset(skip).limit(limit)
    result = await db.execute(query)
    main_accords = result.scalars().all()
    return main_accords

@router.post("/", response_model=MainAccord)
async def create_main_accord(
    *,
    db: AsyncSession = Depends(get_db),
    main_accord_in: MainAccordCreate
):
    """
    Create new main accord.
    """
    query = select(MainAccordModel).filter(MainAccordModel.name == main_accord_in.name)
    result = await db.execute(query)
    db_main_accord = result.scalar_one_or_none()
    
    if db_main_accord:
        raise HTTPException(
            status_code=400,
            detail="Main accord with this name already exists."
        )
    
    db_main_accord = MainAccordModel(name=main_accord_in.name)
    db.add(db_main_accord)
    await db.commit()
    await db.refresh(db_main_accord)
    return db_main_accord

@router.get("/{main_accord_id}", response_model=MainAccord)
async def read_main_accord(
    *,
    db: AsyncSession = Depends(get_db),
    main_accord_id: int
):
    """
    Get main accord by ID.
    """
    query = select(MainAccordModel).filter(MainAccordModel.id == main_accord_id)
    result = await db.execute(query)
    main_accord = result.scalar_one_or_none()
    
    if not main_accord:
        raise HTTPException(
            status_code=404,
            detail="Main accord not found"
        )
    return main_accord

@router.delete("/{main_accord_id}")
async def delete_main_accord(
    *,
    db: AsyncSession = Depends(get_db),
    main_accord_id: int
):
    """
    Delete main accord by ID.
    """
    query = select(MainAccordModel).filter(MainAccordModel.id == main_accord_id)
    result = await db.execute(query)
    main_accord = result.scalar_one_or_none()
    
    if not main_accord:
        raise HTTPException(
            status_code=404,
            detail="Main accord not found"
        )
    
    await db.delete(main_accord)
    await db.commit()
    return {"message": "Main accord deleted successfully"} 