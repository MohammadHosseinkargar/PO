from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession
from src.core.database import get_db
from src.models import Product, StockLevel, StockMovement, MovementType, User, UserRole
from src.schemas import (
    StockLevel as StockLevelSchema,
    StockMovement as StockMovementSchema,
    StockMovementBase,
)
from src.routes.auth import get_current_active_user
from uuid import UUID

router = APIRouter()

@router.get("/levels", response_model=List[StockLevelSchema])
async def list_stock_levels(
    skip: int = Query(0, ge=0),
    limit: int = Query(20, ge=1, le=100),
    product_id: Optional[UUID] = None,
    location: Optional[str] = None,
    low_stock: bool = False,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
) -> List[StockLevel]:
    query = select(StockLevel)
    
    if product_id:
        query = query.where(StockLevel.product_id == product_id)
    if location:
        query = query.where(StockLevel.location == location)
    if low_stock:
        # Join with Product to check min_stock threshold
        query = query.join(Product).where(StockLevel.quantity <= Product.min_stock)
    
    query = query.offset(skip).limit(limit)
    result = await db.execute(query)
    return result.scalars().all()

@router.get("/movements", response_model=List[StockMovementSchema])
async def list_stock_movements(
    skip: int = Query(0, ge=0),
    limit: int = Query(20, ge=1, le=100),
    product_id: Optional[UUID] = None,
    movement_type: Optional[MovementType] = None,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
) -> List[StockMovement]:
    query = select(StockMovement)
    
    if product_id:
        query = query.where(StockMovement.product_id == product_id)
    if movement_type:
        query = query.where(StockMovement.type == movement_type)
    
    query = query.order_by(StockMovement.created_at.desc())
    query = query.offset(skip).limit(limit)
    result = await db.execute(query)
    return result.scalars().all()

@router.post("/movements", response_model=StockMovementSchema)
async def create_stock_movement(
    movement_in: StockMovementBase,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
) -> StockMovement:
    if current_user.role == UserRole.VIEWER:
        raise HTTPException(
            status_code=403,
            detail="Not enough permissions"
        )
    
    # Check if product exists
    product = await db.get(Product, movement_in.product_id)
    if not product:
        raise HTTPException(
            status_code=404,
            detail="Product not found"
        )
    
    # Get or create stock level
    stock_level = await db.execute(
        select(StockLevel).where(
            StockLevel.product_id == movement_in.product_id,
            StockLevel.location == "main"  # Default location
        )
    )
    stock_level = stock_level.scalar_one_or_none()
    
    if not stock_level:
        stock_level = StockLevel(
            product_id=movement_in.product_id,
            quantity=0,
            location="main"
        )
        db.add(stock_level)
    
    # Update stock level based on movement type
    if movement_in.type == MovementType.IN:
        stock_level.quantity += movement_in.quantity
    elif movement_in.type == MovementType.OUT:
        if stock_level.quantity < movement_in.quantity:
            raise HTTPException(
                status_code=400,
                detail="Not enough stock"
            )
        stock_level.quantity -= movement_in.quantity
    else:  # ADJUST
        stock_level.quantity = movement_in.quantity
    
    # Create movement record
    db_movement = StockMovement(**movement_in.model_dump())
    db.add(db_movement)
    
    await db.commit()
    await db.refresh(db_movement)
    
    return db_movement

@router.get("/alerts")
async def get_stock_alerts(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
) -> dict:
    # Get products with stock below minimum level
    query = select(
        Product.id,
        Product.name,
        Product.min_stock,
        func.coalesce(func.sum(StockLevel.quantity), 0).label("total_stock")
    ).outerjoin(StockLevel).group_by(Product.id).having(
        func.coalesce(func.sum(StockLevel.quantity), 0) <= Product.min_stock
    )
    
    result = await db.execute(query)
    alerts = []
    
    for row in result:
        alerts.append({
            "product_id": row.id,
            "product_name": row.name,
            "min_stock": row.min_stock,
            "current_stock": row.total_stock,
        })
    
    return {
        "alerts": alerts,
        "count": len(alerts)
    }