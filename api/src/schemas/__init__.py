from typing import Optional, List, Dict, Any
from datetime import datetime
from uuid import UUID
from pydantic import BaseModel, EmailStr, Field, constr

# Base models
class UserBase(BaseModel):
    email: EmailStr
    name: str
    role: str = "viewer"

class UserCreate(UserBase):
    password: constr(min_length=8)

class UserUpdate(BaseModel):
    email: Optional[EmailStr] = None
    name: Optional[str] = None
    password: Optional[constr(min_length=8)] = None
    role: Optional[str] = None

class User(UserBase):
    id: UUID
    is_active: bool
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

class Token(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"

class TokenData(BaseModel):
    user_id: UUID
    exp: datetime

class ProductBase(BaseModel):
    name: str
    sku: str
    barcode: Optional[str] = None
    description: Optional[str] = None
    category_id: UUID
    cost_price: float = Field(ge=0)
    sale_price: float = Field(ge=0)
    min_stock: int = Field(ge=0, default=0)
    image_url: Optional[str] = None
    attributes: Optional[Dict[str, Any]] = None

class ProductCreate(ProductBase):
    pass

class ProductUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    category_id: Optional[UUID] = None
    cost_price: Optional[float] = Field(None, ge=0)
    sale_price: Optional[float] = Field(None, ge=0)
    min_stock: Optional[int] = Field(None, ge=0)
    image_url: Optional[str] = None
    attributes: Optional[Dict[str, Any]] = None

class Product(ProductBase):
    id: UUID
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

class CategoryBase(BaseModel):
    name: str
    description: Optional[str] = None
    parent_id: Optional[UUID] = None

class CategoryCreate(CategoryBase):
    pass

class Category(CategoryBase):
    id: UUID
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

class StockLevelBase(BaseModel):
    product_id: UUID
    quantity: int = Field(ge=0)
    location: str

class StockLevel(StockLevelBase):
    id: UUID
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

class StockMovementBase(BaseModel):
    product_id: UUID
    type: str  # in, out, adjust
    quantity: int
    reference_id: Optional[UUID] = None
    notes: Optional[str] = None

class StockMovement(StockMovementBase):
    id: UUID
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

class SupplierBase(BaseModel):
    name: str
    contact_name: Optional[str] = None
    email: Optional[EmailStr] = None
    phone: Optional[str] = None
    address: Optional[str] = None
    notes: Optional[str] = None

class SupplierCreate(SupplierBase):
    pass

class Supplier(SupplierBase):
    id: UUID
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

class PurchaseOrderItemBase(BaseModel):
    product_id: UUID
    quantity: int = Field(gt=0)
    unit_price: float = Field(gt=0)

class PurchaseOrderItem(PurchaseOrderItemBase):
    id: UUID
    received_quantity: int = Field(ge=0)
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

class PurchaseOrderBase(BaseModel):
    supplier_id: UUID
    items: List[PurchaseOrderItemBase]
    notes: Optional[str] = None

class PurchaseOrderCreate(PurchaseOrderBase):
    pass

class PurchaseOrder(PurchaseOrderBase):
    id: UUID
    status: str
    total_amount: float
    items: List[PurchaseOrderItem]
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True