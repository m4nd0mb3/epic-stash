from pathlib import Path
from fastapi import UploadFile, File

class StorageService:
    def __init__(self, storage_type: str, base_storage_path:str):
        self.storage_type = storage_type
        self.base_storage_path = Path(base_storage_path)

    def save_file(self, file: UploadFile, bucket_name: str):
        if self.storage_type == "local":
            return self._save_local(file,bucket_name)
        elif self.storage_type == "s3":
            return self._save_s3(file)
        else:
            raise HTTPException(status_code=500, detail="Invalid storage type")

    def _save_local(self, file: UploadFile, bucket_name: str):
        # file_path = os.path.join("uploads", file.filename)
        bucket_path = self.get_bucket_path(bucket_name)
        bucket_path.mkdir(parents=True, exist_ok=True)
        file_path = bucket_path / file.filename

        with open(file_path, "wb") as buffer:
            buffer.write(file.file.read())
        return file_path

    def _save_s3(self, file: UploadFile):
        # Lógica de salvamento no S3
        pass

    def get_bucket_path(self, bucket_name: str) -> Path:
        return self.base_storage_path / bucket_name

    # def upload_file(self, bucket_name: str, file_name: str, file_content: bytes):
    #     bucket_path = self.get_bucket_path(bucket_name)
    #     bucket_path.mkdir(parents=True, exist_ok=True)

    #     file_path = bucket_path / file_name
    #     with open(file_path, 'wb') as file:
    #         file.write(file_content)

    def get_file(self, bucket_name: str, file_name: str) -> bytes:
        file_path = self.get_bucket_path(bucket_name) / file_name
        with open(file_path, 'rb') as file:
            return file.read()

    def list_files(self, bucket_name: str):
        bucket_path = self.get_bucket_path(bucket_name)
        return [file.name for file in bucket_path.iterdir()]

    def delete_file(self, bucket_name: str, file_name: str):
        file_path = self.get_bucket_path(bucket_name) / file_name
        if file_path.exists():
            file_path.unlink()