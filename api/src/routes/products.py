from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query, UploadFile, File
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from src.core.database import get_db
from src.models import Product, Category, User, UserRole
from src.schemas import ProductCreate, ProductUpdate, Product as ProductSchema
from src.routes.auth import get_current_active_user
from uuid import UUID

router = APIRouter()

@router.get("/", response_model=List[ProductSchema])
async def list_products(
    skip: int = Query(0, ge=0),
    limit: int = Query(20, ge=1, le=100),
    category_id: Optional[UUID] = None,
    search: Optional[str] = None,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
) -> List[Product]:
    query = select(Product)
    
    if category_id:
        query = query.where(Product.category_id == category_id)
    if search:
        query = query.where(Product.name.ilike(f"%{search}%"))
    
    query = query.offset(skip).limit(limit)
    result = await db.execute(query)
    return result.scalars().all()

@router.post("/", response_model=ProductSchema)
async def create_product(
    product_in: ProductCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
) -> Product:
    if current_user.role == UserRole.VIEWER:
        raise HTTPException(
            status_code=403,
            detail="Not enough permissions"
        )
    
    # Check if category exists
    category = await db.get(Category, product_in.category_id)
    if not category:
        raise HTTPException(
            status_code=404,
            detail="Category not found"
        )
    
    # Check if SKU is unique
    existing = await db.execute(
        select(Product).where(Product.sku == product_in.sku)
    )
    if existing.scalar_one_or_none():
        raise HTTPException(
            status_code=400,
            detail="SKU already exists"
        )
    
    # Create product
    db_product = Product(**product_in.model_dump())
    db.add(db_product)
    await db.commit()
    await db.refresh(db_product)
    return db_product

@router.get("/{product_id}", response_model=ProductSchema)
async def get_product(
    product_id: UUID,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
) -> Product:
    product = await db.get(Product, product_id)
    if not product:
        raise HTTPException(
            status_code=404,
            detail="Product not found"
        )
    return product

@router.put("/{product_id}", response_model=ProductSchema)
async def update_product(
    product_id: UUID,
    product_in: ProductUpdate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
) -> Product:
    if current_user.role == UserRole.VIEWER:
        raise HTTPException(
            status_code=403,
            detail="Not enough permissions"
        )
    
    product = await db.get(Product, product_id)
    if not product:
        raise HTTPException(
            status_code=404,
            detail="Product not found"
        )
    
    update_data = product_in.model_dump(exclude_unset=True)
    
    # If updating category, check if it exists
    if "category_id" in update_data:
        category = await db.get(Category, update_data["category_id"])
        if not category:
            raise HTTPException(
                status_code=404,
                detail="Category not found"
            )
    
    # Update product attributes
    for field, value in update_data.items():
        setattr(product, field, value)
    
    await db.commit()
    await db.refresh(product)
    return product

@router.delete("/{product_id}")
async def delete_product(
    product_id: UUID,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
) -> dict:
    if current_user.role != UserRole.ADMIN:
        raise HTTPException(
            status_code=403,
            detail="Not enough permissions"
        )
    
    product = await db.get(Product, product_id)
    if not product:
        raise HTTPException(
            status_code=404,
            detail="Product not found"
        )
    
    await db.delete(product)
    await db.commit()
    
    return {"message": "Product deleted successfully"}

@router.post("/{product_id}/image")
async def upload_product_image(
    product_id: UUID,
    file: UploadFile = File(...),
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
) -> dict:
    if current_user.role == UserRole.VIEWER:
        raise HTTPException(
            status_code=403,
            detail="Not enough permissions"
        )
    
    product = await db.get(Product, product_id)
    if not product:
        raise HTTPException(
            status_code=404,
            detail="Product not found"
        )
    
    # TODO: Implement file upload to storage service
    # For now, just return success
    return {"message": "Image uploaded successfully"}