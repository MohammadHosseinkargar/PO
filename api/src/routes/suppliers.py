from typing import List
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from src.core.database import get_db
from src.models import (
    Supplier,
    PurchaseOrder,
    PurchaseOrderItem,
    StockMovement,
    MovementType,
    User,
    UserRole,
)
from src.schemas import (
    SupplierCreate,
    Supplier as SupplierSchema,
    PurchaseOrderCreate,
    PurchaseOrder as PurchaseOrderSchema,
)
from src.routes.auth import get_current_active_user
from uuid import UUID

router = APIRouter()

@router.get("/", response_model=List[SupplierSchema])
async def list_suppliers(
    skip: int = Query(0, ge=0),
    limit: int = Query(20, ge=1, le=100),
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
) -> List[Supplier]:
    query = select(Supplier).offset(skip).limit(limit)
    result = await db.execute(query)
    return result.scalars().all()

@router.post("/", response_model=SupplierSchema)
async def create_supplier(
    supplier_in: SupplierCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
) -> Supplier:
    if current_user.role == UserRole.VIEWER:
        raise HTTPException(
            status_code=403,
            detail="Not enough permissions"
        )
    
    db_supplier = Supplier(**supplier_in.model_dump())
    db.add(db_supplier)
    await db.commit()
    await db.refresh(db_supplier)
    return db_supplier

@router.get("/{supplier_id}", response_model=SupplierSchema)
async def get_supplier(
    supplier_id: UUID,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
) -> Supplier:
    supplier = await db.get(Supplier, supplier_id)
    if not supplier:
        raise HTTPException(
            status_code=404,
            detail="Supplier not found"
        )
    return supplier

@router.get("/{supplier_id}/orders", response_model=List[PurchaseOrderSchema])
async def list_supplier_orders(
    supplier_id: UUID,
    skip: int = Query(0, ge=0),
    limit: int = Query(20, ge=1, le=100),
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
) -> List[PurchaseOrder]:
    query = select(PurchaseOrder).where(
        PurchaseOrder.supplier_id == supplier_id
    ).order_by(
        PurchaseOrder.created_at.desc()
    ).offset(skip).limit(limit)
    
    result = await db.execute(query)
    return result.scalars().all()

@router.post("/orders", response_model=PurchaseOrderSchema)
async def create_purchase_order(
    order_in: PurchaseOrderCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
) -> PurchaseOrder:
    if current_user.role == UserRole.VIEWER:
        raise HTTPException(
            status_code=403,
            detail="Not enough permissions"
        )
    
    # Check if supplier exists
    supplier = await db.get(Supplier, order_in.supplier_id)
    if not supplier:
        raise HTTPException(
            status_code=404,
            detail="Supplier not found"
        )
    
    # Calculate total amount
    total_amount = sum(item.quantity * item.unit_price for item in order_in.items)
    
    # Create purchase order
    db_order = PurchaseOrder(
        supplier_id=order_in.supplier_id,
        status="draft",
        total_amount=total_amount,
        notes=order_in.notes
    )
    db.add(db_order)
    
    # Create purchase order items
    for item in order_in.items:
        db_item = PurchaseOrderItem(
            po_id=db_order.id,
            **item.model_dump()
        )
        db.add(db_item)
    
    await db.commit()
    await db.refresh(db_order)
    return db_order

@router.post("/orders/{order_id}/receive")
async def receive_purchase_order(
    order_id: UUID,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
) -> dict:
    if current_user.role == UserRole.VIEWER:
        raise HTTPException(
            status_code=403,
            detail="Not enough permissions"
        )
    
    order = await db.get(PurchaseOrder, order_id)
    if not order:
        raise HTTPException(
            status_code=404,
            detail="Order not found"
        )
    
    if order.status != "ordered":
        raise HTTPException(
            status_code=400,
            detail="Order must be in 'ordered' status to be received"
        )
    
    # Update order status
    order.status = "received"
    
    # Create stock movements for each item
    for item in order.items:
        movement = StockMovement(
            product_id=item.product_id,
            type=MovementType.IN,
            quantity=item.quantity,
            reference_id=order.id,
            notes=f"Received from PO #{order.id}"
        )
        db.add(movement)
        item.received_quantity = item.quantity
    
    await db.commit()
    
    return {"message": "Purchase order received successfully"}