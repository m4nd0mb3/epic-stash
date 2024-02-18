# storage.py
from app.services.storage_service import StorageService

class StorageConfig:
    BASE_STORAGE_PATH = "./media/uploads/"

storage_service = StorageService(storage_type='local', base_storage_path=StorageConfig.BASE_STORAGE_PATH)
