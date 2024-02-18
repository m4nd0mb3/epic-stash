"""
Roles Endpoints
"""

# pylint: disable=C0103,E0401
from typing import List
from uuid import UUID
from fastapi import APIRouter, status, Depends, HTTPException, Query  # , Response
from sqlalchemy.ext.asyncio import session, AsyncSession
from sqlalchemy.future import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import selectinload
from app.core.deps import (
    get_current_user,
    get_session,
    is_staff
)
from app.models.file import FileModel
from app.schemas.file import (
    FileSchema,
    FileSchemaBase,
    FileSchemaCreate
)

from app.repositories.file import FileRepository
# from app.db.models.user import User

from app.schemas.user import (
    User as UserSchema,
)  # , Response, status

router = APIRouter()




# GET SERIES
@router.get(
    "/",
    response_model=List[FileSchema],
    status_code=200,
    # dependencies=[Depends(is_admin_or_company_manager)],
)
async def get_files(
    db: AsyncSession = Depends(get_session),
    current_user: UserSchema = Depends(get_current_user),
    # company_uuid: UUID = Depends(get_company_uuid),
):
    """
    Get Files
    """

    async with db as session:
        return await FileRepository.get_all(current_user.uuid,session)

# GET SERIES
@router.get(
    "/by-bucket/{bucket_uuid}",
    response_model=List[FileSchema],
    status_code=200,
    # dependencies=[Depends(is_admin_or_company_manager)],
)
async def get_files_by_bucket(
    bucket_uuid:UUID,
    db: AsyncSession = Depends(get_session),
    current_user: UserSchema = Depends(get_current_user),
    # company_uuid: UUID = Depends(get_company_uuid),
):
    """
    Get Files By Buckets
    """

    async with db as session:
        return await FileRepository.get_all_by_bucket(bucket_uuid,session)