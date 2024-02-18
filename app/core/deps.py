"""
Deps: is the responsable to create singleton dependecy to be checked while requests
"""

# pylint: disable=C0103,R0903,E0611
from typing import Generator, List, Optional
from uuid import UUID

from fastapi import Depends, HTTPException, Header, status
from jose import jwt, JWTError

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from pydantic import BaseModel

from app.db.session import Session, SessionLocalTest
from app.core.authentication import oauth2_schema
from app.core.config import settings
from app.models.user import UserModel
from app.schemas.user import User


class TokenData(BaseModel):
    """
    ---
    """

    username: Optional[str] = None


async def get_session() -> Generator:
    """
    Get Session
    Return the session using singleton pattern
    """

    session: AsyncSession = Session()

    try:
        yield session
    finally:
        await session.close()

async def get_session_test() -> Generator:
    """
    Get Session Test
    Return the session using singleton pattern
    """

    async with SessionLocalTest() as session: 
        yield session


async def get_current_user(
    db: Session = Depends(get_session), token: str = Depends(oauth2_schema)
) -> UserModel:
    """
    Get Current User
    Return the current user logged
    """

    credential_exception: HTTPException = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Não foi possível autenticar a credencial",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        payload = jwt.decode(
            token,
            settings.SECRET_KEY,
            algorithms=settings.ALGORITHM,
            options={"verify_aud": False},
        )
        username: str = payload.get("sub")

        if username is None:
            raise credential_exception

        token_data: TokenData = TokenData(username=username)
    except JWTError as e:
        # print(e)
        raise credential_exception from e

    async with db as session:
        query = select(UserModel).filter(UserModel.uuid == str(token_data.username))
        result = await session.execute(query)
        user: UserModel = result.scalars().unique().one_or_none()

        if user is None:
            raise credential_exception
        return user


def is_staff(current_user: Session = Depends(get_current_user)):
    """
    is super user function
    """

    if not current_user.is_staff:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Permissão negada. Acesso permitido apenas para super-user.",
        )

    return current_user


def _verify_permission(roles: List[str], required_roles: List[str]) -> bool:
    """
    _verify_permission
    """
    # return all(role in roles for role in required_roles)
    return any(role in roles for role in required_roles)
