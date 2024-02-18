# tests/unit/test_unit_main.py
from fastapi.testclient import TestClient
from unittest.mock import patch
from main import app

client = TestClient(app)

def test_connection_api_v1():
    # with patch('fastapi.testclient.TestClient.get') as mock_get:
    #     # Configurando o mock para retornar um status code 404
    #     mock_get.return_value.status_code = 404

        # Fazendo a requisição à rota
    response = client.get("/api/v1/")

    # Verificando se a resposta é um status code 404
    assert response.status_code == 200
