"""
PRoducts Schemas
"""

# pylint: disable=R0903,W0107,E0611
from typing import Optional, List, Any
from uuid import UUID
from datetime import datetime, date
from pydantic import UUID1, BaseModel


class AddressSchemaBase(BaseModel):
    """
    Base Address Schema
    """

    name: str
    street: str
    reference_house: str
    longitude: Optional[str]
    latitude: Optional[str]


class AddressSchemaCreate(AddressSchemaBase):
    """
    Address Schema
    """

    saved_by: UUID

    class Config:
        """
        Config Address Schema
        """

        orm_mode = True


class AddressSchema(AddressSchemaBase):
    """
    Address Schema
    """

    uuid: UUID
    is_active: bool = True
    created_at: datetime
    updated_at: datetime
    saved_by: UUID

    class Config:
        """
        Config Address Schema
        """

        orm_mode = True
