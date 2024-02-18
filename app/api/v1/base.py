"""
---
"""

# pylint: disable=C0103,E0611,E0401
from fastapi import APIRouter
from app.api.v1 import conexion

from .endpoints import (
    buckets,
    download,
    files,
    upload,
    users,
)


api_router_v1 = APIRouter()

api_router_v1.include_router(buckets.router, prefix="/buckets", tags=["buckets"])
api_router_v1.include_router(download.router, prefix="/download", tags=["download"])
api_router_v1.include_router(files.router, prefix="/files", tags=["files"])
api_router_v1.include_router(upload.router, prefix="/upload", tags=["upload"])
api_router_v1.include_router(users.router, prefix="/users", tags=["users"])
api_router_v1.include_router(conexion.router)
