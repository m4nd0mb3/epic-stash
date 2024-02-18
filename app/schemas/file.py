"""
PRoducts Schemas
"""

# pylint: disable=R0903,W0107,E0611
from typing import Optional, List, Any
from uuid import UUID
from datetime import datetime, date
from pydantic import BaseModel

from app.schemas.bucket import BucketSchemaBase


class FileSchemaBase(BaseModel):
    """
    Base File Schema
    """

    filename: str
    content_type: str
    size: int


class FileSchemaCreate(FileSchemaBase):
    """
    File Schema
    """

    bucket_uuid: UUID
    saved_by: UUID

    class Config:
        """
        Config File Schema
        """

        orm_mode = True


class FileSchema(FileSchemaBase):
    """
    File Schema
    """

    uuid: UUID
    is_active: bool = True
    created_at: datetime
    updated_at: datetime
    bucket_uuid: UUID
    saved_by: UUID
    bucket: Optional[Any]

    class Config:
        """
        Config File Schema
        """

        orm_mode = True
