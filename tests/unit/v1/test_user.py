# tests/unit/test_unit_main.py
from unittest.mock import patch
from fastapi.testclient import TestClient
from app.core.config import settings
from main import app

client = TestClient(app)

# def test_conexion_api_v1():
#     with patch("main.calculate_square", return_value={"result": 16}):
#         response = client.get("/square/4")

#     assert response.status_code == 200

def test_create_user():
    """
    Test Create User
    With all data is valid
    Return True if all Data is valid and (created or Exist)
    """
    # Crie o objeto de mock para o método create_user
    # mock_create_user = mocker.patch(
    #     "app.apis.v1.endpoints.users.create_user", autospec=True
    # )
    # Defina o comportamento esperado para o mock do método de criação de usuário
    # mock_create_user.return_value = UserModel(
    #     id=1, name="John Doe", email="john@example.com", phone_number="+244912345678"
    # )

    # Faça a solicitação para o aplicativo FastAPI para criar um usuário
    response = client.post(
        settings.API_V1_STR + "/users/",
        json={
            "name": "John Doe",
            "email": "john@example.com",
            "phone_number": "+244912345678",
            "password": "test@pass",
        },
    )

    assert response.status_code in (201, 406)
    # assert response.json() == {
    #     "name": "John Doe",
    #     "email": "john@example.com",
    #     "phone_number": "+244912345678",
    #     "is_active": True,
    # } or response.json() == {
    #     "detail": "Já existe um usuário com este email cadastrado."
    # }


def test_email_on_create_user():
    """
    Test Create User
    If email is not valid
    """

    # Faça a solicitação para o aplicativo FastAPI para criar um usuário
    response = client.post(
        settings.API_V1_STR + "/users/",
        json={
            "name": "John Doe",
            "email": "johnexample.com",
            "phone_number": "+244912345678",
            "password": "test@pass",
        },
    )

    # Verify that the response status code is 422 (Unprocessable Entity)
    assert response.status_code == 422

    # Verify that the response JSON contains the expected error message
    assert response.json() == {
        "detail": [
            {
                "loc": ["body", "email"],
                "msg": "value is not a valid email address",
                "type": "value_error.email",
            }
        ]
    }


def test_not_provided_phone_number_on_create_user():
    """
    Test Create User
    If not provide phone number
    """

    # Faça a solicitação para o aplicativo FastAPI para criar um usuário
    response = client.post(
        settings.API_V1_STR + "/users/",
        json={
            "name": "John Doe",
            "email": "john@example.com",
            # "phone_number": "+244912345678",
            "password": "test@pass",
        },
    )

    # Verify that the response status code is 422 (Unprocessable Entity)
    assert response.status_code == 422

    # Verify that the response JSON contains the expected error message
    assert response.json() == {
        "detail": [
            {
                "loc": ["body", "phone_number"],
                "msg": "field required",
                "type": "value_error.missing",
            }
        ]
    }


def test_not_logged_user():
    """
    Test Create User
    If not provide phone number
    """

    # Faça a solicitação para o aplicativo FastAPI para criar um usuário
    response = client.get(
        settings.API_V1_STR + "/users/current_user",
    )

    # Verify that the response status code is 422 (Unprocessable Entity)
    assert response.status_code == 401

    # Verify that the response JSON contains the expected error message
    assert response.json() == {"detail": "Not authenticated"}