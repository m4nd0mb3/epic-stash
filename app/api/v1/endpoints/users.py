"""
---
"""

# pylint: disable=C0103,E0401
from typing import List
from uuid import UUID
from fastapi import APIRouter, status, Depends, HTTPException  # , Response
from fastapi.security import OAuth2PasswordRequestForm
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from sqlalchemy.ext.asyncio import session, AsyncSession
from sqlalchemy.future import select
from sqlalchemy.exc import IntegrityError
from app.core.authentication import authentication, create_access
from app.core.deps import get_session, get_current_user
from app.core.security import password_generator, verify_password
from app.models.user import UserModel
# from app.models.company import RoleModel
# from app.models.user import User

from app.schemas.user import (
    Role,
    User as UserSchema,
    UserCreate as UserSchemaCreate,
    UserSchemaBase,
    UserWithRoles,
    UserChangePassword
)  # , Response, status

router = APIRouter()


# GET current user
@router.get("/current_user", response_model=UserWithRoles)
async def get_logged_user(
    current_user: UserWithRoles = Depends(get_current_user),
    db: AsyncSession = Depends(get_session),
):
    """
    Return the current logged user
    """

    return current_user


# POST CREATE USER  
@router.post("/", response_model=UserSchema, status_code=201)
async def create_user(
    user_data: UserSchemaCreate, db: AsyncSession = Depends(get_session)
):
    """
    CREATE USER

    * Required field:

        - name
        - email
        - password
        - phone_number
    """

    new_user: UserSchema = UserModel(
        name=user_data.name,
        email=user_data.email,
        phone_number=user_data.phone_number,
        password=password_generator(user_data.password),
    )

    async with db as session:
        try:
            session.add(new_user)
            await session.commit()

            return new_user
        except IntegrityError as e:
            raise HTTPException(
                status_code=status.HTTP_406_NOT_ACCEPTABLE,
                detail="Já existe um usuário com este email cadastrado.",
            ) from e


# GET Usuário
@router.get("/{user_uuid}", response_model=UserSchema)
async def get_user(user_uuid: UUID, db: AsyncSession = Depends(get_session)):
    """
    Get User
    """

    async with db as session:
        query = select(UserModel).filter(
            UserModel.uuid == user_uuid, bool(UserModel.is_active)
        )
        result = await session.execute(query)
        usuario: UserSchema = result.scalars().unique().one_or_none()

        if usuario:
            return usuario
        raise HTTPException(
            detail="Usuário não encontrado", status_code=status.HTTP_404_NOT_FOUND
        )


# POST login


@router.post("/login")
async def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: AsyncSession = Depends(get_session),
):
    """
    Login
    """

    user: UserSchemaBase = await authentication(
        email=form_data.username, password=form_data.password, db=db
    )

    if not user:
        raise HTTPException(
            detail="Dados de acesso incorretos.",
            status_code=status.HTTP_400_BAD_REQUEST,
        )
    return JSONResponse(
        content={
            "access_token": create_access(sub=str(user.uuid)),
            "token_type": "bearer",
            "data": jsonable_encoder(user)
        },
        status_code=status.HTTP_200_OK,
    )



@router.post("/change-password")
async def change_password(
    form_data: UserChangePassword,
    db: AsyncSession = Depends(get_session),
    current_user: UserModel = Depends(get_current_user)
):
    """
    Change Password
    """


    if not verify_password(form_data.current_password, current_user.password):
        raise HTTPException(
            detail="Senha actual invalida.",
            status_code=status.HTTP_400_BAD_REQUEST,
        )
    current_user.password = password_generator(form_data.new_password)
    await db.merge(current_user)
    await db.commit()
    return JSONResponse(
        content="Senha alterada com sucesso!",
        status_code=status.HTTP_200_OK,
    )
