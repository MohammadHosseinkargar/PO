from datetime import datetime
import uuid
from sqlalchemy import Column, String, DateTime, Boolean, ForeignKey, Integer, Float, Enum
from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy.orm import relationship
from src.core.database import Base, TimestampMixin, UUIDMixin
import enum

class UserRole(str, enum.Enum):
    ADMIN = "admin"
    STAFF = "staff"
    VIEWER = "viewer"

class User(Base, UUIDMixin, TimestampMixin):
    __tablename__ = "users"

    email = Column(String, unique=True, index=True, nullable=False)
    name = Column(String, nullable=False)
    hashed_password = Column(String, nullable=False)
    role = Column(Enum(UserRole), default=UserRole.VIEWER, nullable=False)
    is_active = Column(Boolean, default=True)

class Category(Base, UUIDMixin, TimestampMixin):
    __tablename__ = "categories"

    name = Column(String, nullable=False)
    description = Column(String)
    parent_id = Column(UUID(as_uuid=True), ForeignKey("categories.id"), nullable=True)
    
    # Relationships
    parent = relationship("Category", remote_side="Category.id", back_populates="children")
    children = relationship("Category", back_populates="parent")
    products = relationship("Product", back_populates="category")

class Product(Base, UUIDMixin, TimestampMixin):
    __tablename__ = "products"

    name = Column(String, nullable=False)
    sku = Column(String, unique=True, index=True, nullable=False)
    barcode = Column(String, unique=True, index=True)
    description = Column(String)
    category_id = Column(UUID(as_uuid=True), ForeignKey("categories.id"), nullable=False)
    cost_price = Column(Float, nullable=False)
    sale_price = Column(Float, nullable=False)
    min_stock = Column(Integer, default=0)
    image_url = Column(String)
    attributes = Column(JSONB)  # For size, color, material, etc.

    # Relationships
    category = relationship("Category", back_populates="products")
    stock_levels = relationship("StockLevel", back_populates="product")
    stock_movements = relationship("StockMovement", back_populates="product")

class Supplier(Base, UUIDMixin, TimestampMixin):
    __tablename__ = "suppliers"

    name = Column(String, nullable=False)
    contact_name = Column(String)
    email = Column(String)
    phone = Column(String)
    address = Column(String)
    notes = Column(String)

    # Relationships
    purchase_orders = relationship("PurchaseOrder", back_populates="supplier")

class StockLevel(Base, UUIDMixin, TimestampMixin):
    __tablename__ = "stock_levels"

    product_id = Column(UUID(as_uuid=True), ForeignKey("products.id"), nullable=False)
    quantity = Column(Integer, default=0)
    location = Column(String, nullable=False)

    # Relationships
    product = relationship("Product", back_populates="stock_levels")

class MovementType(str, enum.Enum):
    IN = "in"        # Purchase
    OUT = "out"      # Sale
    ADJUST = "adjust" # Manual adjustment

class PurchaseOrderStatus(str, enum.Enum):
    DRAFT = "draft"
    ORDERED = "ordered"
    RECEIVED = "received"
    CANCELLED = "cancelled"

class StockMovement(Base, UUIDMixin, TimestampMixin):
    __tablename__ = "stock_movements"

    product_id = Column(UUID(as_uuid=True), ForeignKey("products.id"), nullable=False)
    type = Column(Enum(MovementType), nullable=False)
    quantity = Column(Integer, nullable=False)
    reference_id = Column(UUID(as_uuid=True))  # ID of PO or Sale
    notes = Column(String)

    # Relationships
    product = relationship("Product", back_populates="stock_movements")

class PurchaseOrder(Base, UUIDMixin, TimestampMixin):
    __tablename__ = "purchase_orders"

    supplier_id = Column(UUID(as_uuid=True), ForeignKey("suppliers.id"), nullable=False)
    status = Column(String, nullable=False)  # draft, ordered, received, cancelled
    total_amount = Column(Float, nullable=False)
    notes = Column(String)

    # Relationships
    supplier = relationship("Supplier", back_populates="purchase_orders")
    items = relationship("PurchaseOrderItem", back_populates="purchase_order")

class PurchaseOrderItem(Base, UUIDMixin, TimestampMixin):
    __tablename__ = "purchase_order_items"

    po_id = Column(UUID(as_uuid=True), ForeignKey("purchase_orders.id"), nullable=False)
    product_id = Column(UUID(as_uuid=True), ForeignKey("products.id"), nullable=False)
    quantity = Column(Integer, nullable=False)
    unit_price = Column(Float, nullable=False)
    received_quantity = Column(Integer, default=0)

    # Relationships
    purchase_order = relationship("PurchaseOrder", back_populates="items")
    product = relationship("Product")