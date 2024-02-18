# repositories.py
from uuid import UUID
from sqlalchemy.orm import selectinload, joinedload, contains_eager
from sqlalchemy.future import select
from fastapi import APIRouter, status, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.deps import (
    get_current_user,
    get_session,
    is_staff,
)
from app.models.bucket import BucketModel
from app.models.file import FileModel
from app.schemas.file import FileSchema, FileSchemaBase, FileSchemaCreate

class FileRepository:
    @staticmethod
    async def get_all(user_uuid:UUID, db: AsyncSession):
        async with db as session:
            query = (
                select(FileModel).filter(FileModel.is_active, FileModel.saved_by==user_uuid)
                .join(BucketModel, BucketModel.uuid == FileModel.bucket_uuid)
                .options(
                    joinedload(FileModel.bucket)
                )
            )
            result = await session.execute(query)
            files: List[FileSchema] = result.scalars().unique().all()
            return files

    @staticmethod
    async def get_all_by_bucket(bucket_uuid:UUID, db: AsyncSession):
        async with db as session:
            query = (
                select(FileModel)
                .filter(FileModel.is_active, FileModel.bucket_uuid==bucket_uuid)
                .join(BucketModel, BucketModel.uuid == FileModel.bucket_uuid)
                .options(
                    joinedload(FileModel.bucket)
                )
            )
            result = await session.execute(query)
            files: List[FileSchema] = result.scalars().unique().all()
            return files


    @staticmethod
    async def get_file(file_uuid: UUID, db: AsyncSession):
        query = select(FileModel).filter(bool(FileModel.is_active), FileModel.uuid == file_uuid)
        result = await db.execute(query)
        return result.scalar()

    # @staticmethod
    # def get_file_by_id(db: AsyncSession = Depends(get_session), file_uuid: UUID):
    #     return db.query(FileModel).filter(FileModel.uuid == file_uuid).first()

    @staticmethod
    async def save(file: FileModel, db: AsyncSession):
        if file.uuid:
            await db.merge(file)
        else:
            db.add(file)
        await db.commit()
        await db.refresh(file)
        return file

