from sqlalchemy import Column, String, Integer
from sqlalchemy.orm import relationship
from app.models.base import BaseModelWithUser

class BucketModel(BaseModelWithUser):
    __tablename__ = 'buckets'

    name = Column(String, unique=True, index=True, nullable=False)
    description = Column(String)

    # files = relationship("FileModel")