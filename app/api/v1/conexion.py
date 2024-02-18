"""
---
"""

from fastapi import APIRouter, Response, status

router = APIRouter()


# GET current user
@router.get("/")
def is_online():
    """
    is_online:
        - endpoint to verify if api/v1 still online
    """
    return Response(status_code=status.HTTP_200_OK)
