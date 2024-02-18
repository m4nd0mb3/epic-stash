from fastapi import UploadFile, File, Depends, HTTPException, APIRouter
from fastapi.responses import JSONResponse
from sqlalchemy.ext.asyncio import session, AsyncSession
from starlette import status
from app.core.storage import storage_service
from pathlib import Path
import shutil
from uuid import UUID
from app.core.deps import (
    get_current_user,
    get_session,
    is_staff
)
from app.schemas.user import (
    User as UserSchema,
)  # , Response, status
from app.models.file import FileModel
from app.repositories.file import FileRepository
from app.repositories.bucket import BucketRepository
from app.schemas.file import FileSchema, FileSchemaBase, FileSchemaCreate
router = APIRouter()


@router.post("/{bucket_uuid}")
async def upload_file(
    bucket_uuid:UUID,file: UploadFile = File(...), 
    current_user: UserSchema = Depends(get_current_user),
    db: AsyncSession = Depends(get_session)):

    async with db as session:
        try:
            # Salvar o arquivo no diretório de armazenamento
            # file_path = storage_directory / file.filename
            # with file_path.open("wb") as buffer:
            #     shutil.copyfileobj(file.file, buffer)
            bucket = await BucketRepository.get_bucket(bucket_uuid, session)
            if not bucket:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Bucket não encotrada!",
                )
            new_file:FileSchemaCreate = FileModel(
                filename=file.filename,
                content_type=file.content_type,
                size=file.size,
                bucket_uuid=bucket.uuid,
                saved_by=current_user.uuid
            )
            storage_service.save_file(file, bucket.name)
            return await FileRepository.save(new_file, session)
            return JSONResponse(content={"message": "Arquivo enviado com sucesso!"})
        except Exception as e:
            storage_service.delete_file(bucket.name, file.filename)
            await session.rollback()
            await session.commit()
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Erro ao processar o arquivo: {str(e)}",
            )
