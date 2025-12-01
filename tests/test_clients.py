# tests/test_clients.py

from fastapi.testclient import TestClient
from tests.conftest import client # Importa el fixture del cliente de prueba

# Usamos el cliente de prueba de FastAPI
# El token debería ser manejado por un fixture más complejo, 
# pero por ahora, asumiremos un token válido 'MOCK_TOKEN' o lo inyectamos en el cliente.
# Dado que tu backend usa `check_token`, debemos pasar un header de autenticación.

MOCK_HEADERS = {"Authorization": "Bearer mock-test-token"} # Ajusta según tu lógica de autenticación

def test_create_client(client: TestClient):
    # 1. Crear un nuevo cliente
    response = client.post(
        "/v1/clients/",
        headers=MOCK_HEADERS,
        json={
            "name": "Test Client 1",
            "email": "test1@example.com",
            "phone": "1234567890"
        }
    )
    
    assert response.status_code == 201
    data = response.json()
    assert data["name"] == "Test Client 1"
    assert "id" in data
    
    # Guardar el ID para las siguientes pruebas
    return data["id"]

def test_list_and_filter_clients(client: TestClient):
    # Aseguramos que existe al menos un cliente
    client_id = test_create_client(client)
    
    # 2. Listar todos los clientes (debería incluir al menos 1)
    response = client.get("/v1/clients/", headers=MOCK_HEADERS)
    
    assert response.status_code == 200
    assert len(response.json()) >= 1
    
    # 3. Filtrar por nombre (ej: name=Test)
    response_filter = client.get("/v1/clients/", params={"name": "Test"}, headers=MOCK_HEADERS)
    
    assert response_filter.status_code == 200
    assert len(response_filter.json()) >= 1
    assert response_filter.json()[0]["name"] == "Test Client 1"
    
def test_update_client(client: TestClient):
    client_id = test_create_client(client)
    
    # 4. Actualizar cliente
    response = client.put(
        f"/v1/clients/{client_id}",
        headers=MOCK_HEADERS,
        json={
            "name": "Updated Client Name",
            "email": "updated@example.com",
            "phone": "0987654321"
        }
    )
    
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "Updated Client Name"

def test_delete_client(client: TestClient):
    client_id = test_create_client(client)
    
    # 5. Eliminar cliente
    response = client.delete(f"/v1/clients/{client_id}", headers=MOCK_HEADERS)
    
    assert response.status_code == 204 # El código de éxito para DELETE es 204 No Content

    # 6. Verificar que el cliente ya no existe
    response_get = client.get(f"/v1/clients/{client_id}", headers=MOCK_HEADERS)
    assert response_get.status_code == 404 # No encontrado