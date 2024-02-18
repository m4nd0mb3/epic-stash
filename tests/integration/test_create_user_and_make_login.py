# tests/integration/test_integration_main.py
import pytest
import pytest_asyncio
import requests
from fastapi.testclient import TestClient
from fastapi.security import OAuth2PasswordRequestForm
from app.core.config import settings
from sqlalchemy.ext.asyncio import AsyncSession
from main import app
from app.db.session import engine_test
from app.core.deps import get_session_test, get_session
from app.models.base import BaseModel
# from sqlalchemy import create_engine
# from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import declarative_base

client = TestClient(app)

Base = BaseModel #declarative_base()
app.dependency_overrides[get_session] = get_session_test

@pytest.fixture()
async def db() -> AsyncSession:
    import app.models.metadata
    async with engine_test.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    # async with get_session_test() as session:
        # await client.create_tables()
        yield session
        # await client.drop_tables()
# Fixture para criar tabelas antes dos testes
@pytest.fixture(scope="function", autouse=True)
# @pytest.fixture(scope="session", autouse=True)
async def create_test_tables()->AsyncSession:
    # import app.models.metadata
    async with engine_test.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    # Executa os testes
    yield

    async with get_session_test() as session:
        await session.rollback()
    # Limpa as tabelas após os testes
    # async with engine_test.begin() as conn:
    #     await conn.run_sync(Base.metadata.drop_all)
# import app.models.metadata
# Base.metadata.create_all(bind=engine_test)
@pytest.mark.asyncio
async def test_integration_create_user_and_make_login():
    # Limpa o banco de dados antes do teste
    # engine = create_engine(DATABASE_URL)
    # Base.metadata.drop_all(bind=engine)
    # Base.metadata.create_all(bind=engine)
    # Cria um usuário
    user_data = {
        "name": "John Doe",
        "email": "john@example.com",
        "phone_number": "+244912345678",
        "password": "test@pass",
    }
    create_response = client.post(settings.API_V1_STR + "/users/", json=user_data)
    assert create_response.status_code == 201
    created_user = create_response.json()
    assert created_user["name"] == user_data["name"]
    assert created_user["uuid"] is not None

    # Fazer Login
    data = OAuth2PasswordRequestForm(username=user_data['email'], password=user_data['password'])
    response = client.post("/users/login", data=data)
    assert response.status_code == 200
    user = response.json()
    assert user["name"] == user_data["name"]
    assert user["uuid"] == created_user["uuid"]
