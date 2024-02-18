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
from app.models.bucket import BucketModel
from app.schemas.bucket import (
    BucketSchema,
    BucketSchemaBase,
    BucketSchemaCreate
)

from app.repositories.bucket import BucketRepository
# from app.db.models.user import User

from app.schemas.user import (
    User as UserSchema,
)  # , Response, status

router = APIRouter()


# CREATE SERIE
@router.post(
    "/",
    response_model=BucketSchema,
    status_code=201,
    # dependencies=[Depends(is_staff)],
)
async def create_bucket(
    bucket_data: BucketSchemaBase,
    db: AsyncSession = Depends(get_session),
    current_user: UserSchema = Depends(get_current_user),
    # company_uuid: UUID = Depends(get_company_uuid),
):
    """
    ADD NEW BUCKET

    * Required field:

        - name
        - description
        - ...
    """

    new_bucket: BucketSchemaCreate = BucketModel(
        name=bucket_data.name,
        description=bucket_data.description,
        saved_by=current_user.uuid,
    )

    async with db as session:
        try:
            return await BucketRepository.save(new_bucket, session)
        except IntegrityError as e:
            raise HTTPException(
                status_code=status.HTTP_406_NOT_ACCEPTABLE,
                detail="Bucket inavalido!",
            ) from e

# CREATE SERIE
@router.put(
    "/{bucket_uuid}",
    response_model=BucketSchema,
    status_code=200,
    # dependencies=[Depends(is_staff)],
)
async def update_bucket(
    bucket_uuid:UUID,
    bucket_data: BucketSchemaBase,
    db: AsyncSession = Depends(get_session),
    current_user: UserSchema = Depends(get_current_user),
    # company_uuid: UUID = Depends(get_company_uuid),
):
    """
    UPDATE CATEGORY
    """


    async with db as session:
        try:
            bucket = await BucketRepository.get_bucket(bucket_uuid, session)
            if not bucket:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Bucket não encotrada!",
                )
            
            bucket.name=bucket_data.name
            bucket.description=bucket_data.description

            return await BucketRepository.save(bucket, session)
        except IntegrityError as e:
            raise HTTPException(
                status_code=status.HTTP_406_NOT_ACCEPTABLE,
                detail="Categoria inavalido!",
            ) from e


# GET SERIES
@router.get(
    "/",
    response_model=List[BucketSchema],
    status_code=200,
    # dependencies=[Depends(is_admin_or_company_manager)],
)
async def get_buckets(
    db: AsyncSession = Depends(get_session),
    current_user: UserSchema = Depends(get_current_user),
    # company_uuid: UUID = Depends(get_company_uuid),
):
    """
    Get Buckets
    """

    async with db as session:
        return await BucketRepository.get_all(session)

