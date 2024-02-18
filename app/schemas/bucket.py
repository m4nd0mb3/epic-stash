"""
PRoducts Schemas
"""

# pylint: disable=R0903,W0107,E0611
from typing import Optional, List, Any
from uuid import UUID
from datetime import datetime, date
from pydantic import BaseModel


class BucketSchemaBase(BaseModel):
    """
    Base Bucket Schema
    """

    name: str
    description: str


class BucketSchemaCreate(BucketSchemaBase):
    """
    Bucket Schema
    """

    saved_by: UUID

    class Config:
        """
        Config Bucket Schema
        """

        orm_mode = True


class BucketSchema(BucketSchemaBase):
    """
    Bucket Schema
    """

    uuid: UUID
    is_active: bool = True
    created_at: datetime
    updated_at: datetime
    saved_by: UUID

    class Config:
        """
        Config Bucket Schema
        """

        orm_mode = True


class ProductSchemaBase(BaseModel):
    """
    Base Product Schema
    """

    name: str
    code: Optional[str]
    image: Optional[str]
    price: float
    description: str
    product_type: str = 'P' or 'S' or 'O' or 'E'
    # tax_uuid: UUID
    # category_uuid: Optional[UUID]
    Bucket_uuid: Optional[UUID]
    is_active: Optional[bool]


class ProductSchemaCreate(ProductSchemaBase):
    """
    Product Schema
    """

    saved_by: UUID

    class Config:
        """
        Config Product Schema
        """

        orm_mode = True


class ProductSchema(ProductSchemaBase):
    """
    Product Schema
    """

    uuid: UUID
    is_active: bool = True
    created_at: datetime
    updated_at: datetime
    saved_by: UUID

    class Config:
        """
        Config Product Schema
        """

        orm_mode = True

class ProductToStockMovimentSchema(BaseModel):
    """
    Product Schema
    """

    uuid: UUID
    name: str
    code: Optional[str]
    image: Optional[str]
    price: float
    description: str
    is_stocked: Optional[bool]

    class Config:
        """
        Config Product Schema
        """

        orm_mode = True
