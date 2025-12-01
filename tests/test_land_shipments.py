from fastapi.testclient import TestClient
from datetime import date, timedelta
from tests.conftest import client

MOCK_HEADERS = {"Authorization": "Bearer mock-test-token"}

def create_mock_client(client: TestClient):
    response = client.post("/v1/clients/", headers=MOCK_HEADERS, json={"name": "Test Client", "email": "test@example.com", "phone": "123"})
    assert response.status_code in [201, 200]
    return response.json()["id"]

def create_mock_product(client: TestClient):
    response = client.post("/v1/products/", headers=MOCK_HEADERS, json={"name": "Test Product", "description": "Test"})
    assert response.status_code in [201, 200]
    return response.json()["id"]

def create_mock_warehouse(client: TestClient):
    response = client.post("/v1/warehouses/", headers=MOCK_HEADERS, json={"name": "Test Warehouse", "location": "Location"})
    assert response.status_code in [201, 200]
    return response.json()["id"]

def test_create_shipment_no_discount(client: TestClient):
    client_id = create_mock_client(client)
    product_id = create_mock_product(client)
    warehouse_id = create_mock_warehouse(client)
    
    response = client.post(
        "/v1/land-shipments/",
        headers=MOCK_HEADERS,
        json={
            "client_id": client_id,
            "product_id": product_id,
            "warehouse_id": warehouse_id,
            "quantity": 5, 
            "register_date": "2025-12-01",
            "delivery_date": "2025-12-10",
            "price": 1000.0,
            "plate": "ABC123", 
            "guide_number": "GUIDE00001" 
        }
    )
    
    assert response.status_code == 201
    data = response.json()
    
    assert data["discount"] == 0.0
    assert data["final_price"] == 5000.0 
    

def test_create_shipment_with_discount(client: TestClient):
    client_id = create_mock_client(client)
    product_id = create_mock_product(client)
    warehouse_id = create_mock_warehouse(client)

    response = client.post(
        "/v1/land-shipments/",
        headers=MOCK_HEADERS,
        json={
            "client_id": client_id,
            "product_id": product_id,
            "warehouse_id": warehouse_id,
            "quantity": 12, 
            "register_date": "2025-12-01",
            "delivery_date": "2025-12-10",
            "price": 1000.0,
            "plate": "XYZ789",
            "guide_number": "GUIDE00002"
        }
    )
    
    assert response.status_code == 201
    data = response.json()
    
    assert data["discount"] == 600.0 
    assert data["final_price"] == 11400.0

# --- Pruebas de Filtrado por Fechas ---

def test_list_shipments_filter_by_date(client: TestClient):
    client_id = create_mock_client(client)
    product_id = create_mock_product(client)
    warehouse_id = create_mock_warehouse(client)
    
    test_date_str = "2025-01-15"
    response_create = client.post(
        "/v1/land-shipments/",
        headers=MOCK_HEADERS,
        json={
            "client_id": client_id,
            "product_id": product_id,
            "warehouse_id": warehouse_id,
            "quantity": 1,
            "register_date": test_date_str,
            "delivery_date": "2025-01-20",
            "price": 100.0,
            "plate": "DAT001", 
            "guide_number": "GUIDE00003" 
        }
    )
    assert response_create.status_code == 201 

    response_filter = client.get(
        "/v1/land-shipments/", 
        headers=MOCK_HEADERS, 
        params={"date_from": test_date_str, "date_to": test_date_str}
    )
    
    assert response_filter.status_code == 200
    data_filtered = response_filter.json()
    assert any(item['guide_number'] == "GUIDE00003" for item in data_filtered)


def test_list_shipments_filter_by_plate_and_guide(client: TestClient):
    client_id = create_mock_client(client)
    product_id = create_mock_product(client)
    warehouse_id = create_mock_warehouse(client)

    response_create = client.post(
        "/v1/land-shipments/",
        headers=MOCK_HEADERS,
        json={
            "client_id": client_id,
            "product_id": product_id,
            "warehouse_id": warehouse_id,
            "quantity": 1,
            "register_date": "2025-03-01",
            "delivery_date": "2025-03-10",
            "price": 100.0,
            "plate": "ABC789", 
            "guide_number": "SHIPGUIDE0" 
        }
    )
    assert response_create.status_code == 201

    response_plate = client.get(
        "/v1/land-shipments/", 
        headers=MOCK_HEADERS, 
        params={"plate": "ABC"}
    )
    assert response_plate.status_code == 200
    assert any(item['plate'] == "ABC789" for item in response_plate.json())
    
    response_guide = client.get(
        "/v1/land-shipments/", 
        headers=MOCK_HEADERS, 
        params={"guide_number": "GUIDE0"}
    )
    assert response_guide.status_code == 200
    assert any(item['guide_number'] == "SHIPGUIDE0" for item in response_guide.json())