from fastapi import UploadFile, File, Depends, HTTPException, APIRouter
from fastapi.responses import JSONResponse, FileResponse
from sqlalchemy.ext.asyncio import session, AsyncSession
from starlette import status
from pathlib import Path
import shutil
from uuid import UUID
from app.core.deps import (
    get_current_user,
    get_session,
    is_staff
)
from app.core.storage import storage_service
from app.repositories.bucket import BucketRepository
from app.repositories.file import FileRepository
from app.schemas.bucket import (
    BucketSchema,
    BucketSchemaBase,
    BucketSchemaCreate
)
from app.schemas.file import (
    FileSchema,
    FileSchemaBase,
    FileSchemaCreate
)
router = APIRouter()



@router.get("/{file_uuid}")
async def download_file(file_uuid:UUID,db: AsyncSession = Depends(get_session)):
     async with db as session:
        try:
            file:FileSchema = await FileRepository.get_file(file_uuid, session)
            if not file:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="File não encotrada!",
                )
            file_name = file.filename
            bucket = await BucketRepository.get_bucket(file.bucket_uuid, session)
            if not bucket:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Bucket não encotrada!",
                )
            
            response: JSONResponse = FileResponse(path=storage_service.get_bucket_path(bucket.name) / file_name)
            response.headers["Content-Disposition"] = f"attachment; filename={file_name}"
            response.status_code = status.HTTP_200_OK
            response.body = storage_service.get_file(bucket.name, file_name)
            return response
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Erro ao baixar o arquivo: {str(e)}",
            )
