# repositories.py
from uuid import UUID
from sqlalchemy.orm import Session
from sqlalchemy.future import select
from fastapi import APIRouter, status, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.deps import (
    get_current_user,
    get_session,
    is_staff,
)
from app.models.bucket import BucketModel
from app.schemas.bucket import BucketSchema, BucketSchemaBase, BucketSchemaCreate

class BucketRepository:
    @staticmethod
    async def get_all(db: AsyncSession):
        async with db as session:
            query = select(BucketModel).filter(BucketModel.is_active)
            result = await session.execute(query)
            buckets: List[BucketSchema] = result.scalars().unique().all()
            return buckets


    @staticmethod
    async def get_bucket(bucket_uuid: UUID, db: AsyncSession):
        query = select(BucketModel).filter(bool(BucketModel.is_active), BucketModel.uuid == bucket_uuid)
        result = await db.execute(query)
        return result.scalar()

    # @staticmethod
    # def get_Bucket_by_id(db: AsyncSession = Depends(get_session), bucket_uuid: UUID):
    #     return db.query(BucketModel).filter(BucketModel.uuid == bucket_uuid).first()

    @staticmethod
    async def save(bucket: BucketModel, db: AsyncSession):
        if bucket.uuid:
            await db.merge(bucket)
        else:
            db.add(bucket)
        await db.commit()
        await db.refresh(bucket)
        return bucket

