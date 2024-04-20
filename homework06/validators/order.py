from pydantic import BaseModel, Field
from datetime import datetime
from enum import Enum


class OrderStatus(str, Enum):
    PENDING: str = 'pending'
    PROCESSING: str = 'processing'
    SHIPPED: str = 'shipped'
    DELIVERED: str = 'delivered'
    CANCELLED: str = 'cancelled'


class OrderIn(BaseModel):
    user_id: int = Field(..., ge=0)
    product_id: int = Field(..., ge=0)
    status: OrderStatus = Field(default=OrderStatus.PENDING)


class OrderOut(BaseModel):
    id: int
    user_id: int
    product_id: int
    date: datetime
    status: str
