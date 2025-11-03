from sqlalchemy import Column, String, Boolean, ForeignKey, Numeric, Integer, Text, Enum as SQLEnum
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID
import uuid
from datetime import datetime
from .base import Base, TimestampMixin
from enum import Enum

class PurchaseOrderStatus(str, Enum):
    DRAFT = "draft"
    ORDERED = "ordered"
    RECEIVED = "received"
    CANCELLED = "cancelled"

class Supplier(Base, TimestampMixin):
    __tablename__ = "suppliers"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String(255), nullable=False)
    contact_person = Column(String(255))
    email = Column(String(255))
    phone = Column(String(50))
    address = Column(Text)
    notes = Column(Text)
    is_active = Column(Boolean, default=True)

    purchase_orders = relationship("PurchaseOrder", back_populates="supplier")

    def __repr__(self):
        return f"<Supplier {self.name}>"

class PurchaseOrder(Base, TimestampMixin):
    __tablename__ = "purchase_orders"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    supplier_id = Column(UUID(as_uuid=True), ForeignKey("suppliers.id"), nullable=False)
    status = Column(SQLEnum(PurchaseOrderStatus), nullable=False, default=PurchaseOrderStatus.DRAFT)
    total_amount = Column(Numeric(10, 2), nullable=False)
    notes = Column(Text)

    supplier = relationship("Supplier", back_populates="purchase_orders")
    items = relationship("PurchaseOrderItem", back_populates="purchase_order")

    def __repr__(self):
        return f"<PurchaseOrder {self.id}>"

class PurchaseOrderItem(Base, TimestampMixin):
    __tablename__ = "purchase_order_items"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    po_id = Column(UUID(as_uuid=True), ForeignKey("purchase_orders.id"), nullable=False)
    product_id = Column(UUID(as_uuid=True), ForeignKey("products.id"), nullable=False)
    quantity = Column(Integer, nullable=False)
    unit_price = Column(Numeric(10, 2), nullable=False)
    received_quantity = Column(Integer)
    notes = Column(Text)

    purchase_order = relationship("PurchaseOrder", back_populates="items")
    product = relationship("Product", back_populates="po_items")

    def __repr__(self):
        return f"<PurchaseOrderItem {self.id}>"