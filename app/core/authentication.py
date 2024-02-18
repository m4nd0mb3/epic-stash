"""
Auth
"""

# pylint: disable=C0103,E0611
from typing import Optional
from datetime import datetime, timedelta
from pydantic import EmailStr
from pytz import timezone

from fastapi.security import OAuth2PasswordBearer
from sqlalchemy import and_
from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession

from jose import jwt
from app.common.utils import is_email

from app.models.user import UserModel
from app.core.config import settings
from app.core.security import verify_password
from app.schemas.user import UserSchemaBase


oauth2_schema = OAuth2PasswordBearer(tokenUrl=f"{settings.API_V1_STR}/users/login")


async def authentication(
    email: EmailStr or str, password: str, db: AsyncSession
) -> Optional[UserSchemaBase]:
    """
    Authentication Function
    """

    async with db as session:
        query = select(UserModel).filter(
            and_(
                UserModel.is_active,
                UserModel.email == email
                if is_email(email)
                else UserModel.phone_number == email,
            )
        )
        result = await session.execute(query)
        usuario: UserSchemaBase = result.scalar()

        if not usuario:
            return None

        if not verify_password(password, usuario.password):
            return None

        return usuario


def _create_token(token_type: str, time_to_live: timedelta, sub: str) -> str:
    payload = {}  # https://datatrucker.ietf.org/doc/html/rfc7519#section-4.1.3
    luanda = timezone("Africa/Luanda")
    expire = datetime.now(tz=luanda) + time_to_live

    payload["type"] = token_type
    payload["exp"] = expire
    payload["iat"] = datetime.now(tz=luanda)
    payload["sub"]: str = sub

    return jwt.encode(payload, settings.SECRET_KEY, algorithm=settings.ALGORITHM)


def create_access(sub: str) -> str:
    """
    https://jwt.io
    """
    return _create_token(
        token_type="access_token",
        time_to_live=timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES),
        sub=sub,
    )
