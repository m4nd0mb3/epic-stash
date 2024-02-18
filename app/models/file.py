from sqlalchemy import Column, String, Integer, ForeignKey, UUID
from sqlalchemy.orm import relationship
from app.models.base import BaseModelWithUser

class FileModel(BaseModelWithUser):
    __tablename__ = 'files'

    filename = Column(String, nullable=False)
    content_type = Column(String, nullable=False)
    size = Column(Integer, nullable=False)
    bucket_uuid = Column(UUID, ForeignKey('buckets.uuid'), nullable=False)
    
    # Relacionamento com o modelo de Bucket
    bucket = relationship("BucketModel")