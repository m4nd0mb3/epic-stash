"""
---
"""

from datetime import datetime, timedelta
from typing import Optional
from jose import jwt
from passlib.context import CryptContext
from .config import settings


CRYPTO = CryptContext(schemes=["bcrypt"], deprecated="auto")


async def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    """---"""
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(
            minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES
        )
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(
        to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM
    )
    return encoded_jwt


def verify_password(password: str, hash_password: str) -> bool:
    """
    Função para verificar se a senha está correta, comparando a
    senha em texto puro, informada pelo usuário, e o hash da
    senha que estará salvo no banco de dados durante a criação
    da conta.
    """

    return CRYPTO.verify(password, hash_password)


def password_generator(password: str) -> str:
    """
    Função que gera e retorna o hash da senha
    """

    return CRYPTO.hash(password)
