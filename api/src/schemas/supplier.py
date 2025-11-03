from typing import List, Optional
from uuid import UUID
from pydantic import BaseModel, EmailStr, constr
from decimal import Decimal

class SupplierBase(BaseModel):
    name: constr(min_length=1, max_length=255)
    contact_person: Optional[str] = None
    email: Optional[EmailStr] = None
    phone: Optional[str] = None
    address: Optional[str] = None
    notes: Optional[str] = None

class SupplierCreate(SupplierBase):
    pass

class Supplier(SupplierBase):
    id: UUID
    is_active: bool

    class Config:
        from_attributes = True

class PurchaseOrderItemBase(BaseModel):
    product_id: UUID
    quantity: int
    unit_price: Decimal
    notes: Optional[str] = None

class PurchaseOrderItem(PurchaseOrderItemBase):
    id: UUID
    po_id: UUID
    received_quantity: Optional[int] = None

    class Config:
        from_attributes = True

class PurchaseOrderItemCreate(PurchaseOrderItemBase):
    pass

class PurchaseOrderBase(BaseModel):
    supplier_id: UUID
    notes: Optional[str] = None

class PurchaseOrderCreate(PurchaseOrderBase):
    items: List[PurchaseOrderItemCreate]

class PurchaseOrder(PurchaseOrderBase):
    id: UUID
    status: str  # draft, ordered, received, cancelled
    total_amount: Decimal
    items: List[PurchaseOrderItem]
    created_at: str
    updated_at: str

    class Config:
        from_attributes = True