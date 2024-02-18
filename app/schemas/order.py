"""
PRoducts Schemas
"""

# pylint: disable=R0903,W0107,E0611
from typing import Optional, List, Any
from uuid import UUID
from datetime import datetime, date
from pydantic import UUID1, BaseModel


class OrderProductSchemaBase(BaseModel):
    """
    Base OrderProduct Schema
    """

    product_uuid: UUID
    quantity: int


class OrderProductSchemaCreate(OrderProductSchemaBase):
    """
    OrderProduct Schema
    """

    order_uuid: UUID
    saved_by: UUID

    class Config:
        """
        Config OrderProduct Schema
        """

        orm_mode = True


class OrderProductSchema(OrderProductSchemaBase):
    """
    OrderProduct Schema
    """

    uuid: UUID
    is_active: bool = True
    order_uuid: UUID
    product: Any
    # saved_by: UUID

    class Config:
        """
        Config OrderProduct Schema
        """

        orm_mode = True

class OrderSchemaBase(BaseModel):
    """
    Base Order Schema
    """

    # customer_uuid: UUID
    products: List[OrderProductSchemaBase]


class OrderSchemaCreate(OrderSchemaBase):
    """
    Order Schema
    """

    saved_by: UUID

    class Config:
        """
        Config Order Schema
        """

        orm_mode = True


class OrderSchema(OrderSchemaBase):
    """
    Order Schema
    """

    uuid: UUID
    is_active: bool = True
    created_at: datetime
    updated_at: datetime
    order_date: datetime
    saved_by: UUID
    products: List[OrderProductSchema]

    class Config:
        """
        Config Order Schema
        """

        orm_mode = True

