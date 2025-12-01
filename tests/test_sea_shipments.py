from fastapi.testclient import TestClient
from tests.conftest import client

MOCK_HEADERS = {"Authorization": "Bearer mock-test-token"}


def create_mock_client(client: TestClient):
    response = client.post("/v1/clients/", headers=MOCK_HEADERS, json={"name": "Test Client Sea", "email": "test-sea@example.com", "phone": "456"})
    assert response.status_code in [201, 200]
    return response.json()["id"]

def create_mock_product(client: TestClient):
    response = client.post("/v1/products/", headers=MOCK_HEADERS, json={"name": "Test Product Sea", "description": "Test Sea"})
    assert response.status_code in [201, 200]
    return response.json()["id"]

def create_mock_port(client: TestClient):
    response = client.post("/v1/ports/", headers=MOCK_HEADERS, json={"name": "Test Port", "location": "Ocean Location"})
    assert response.status_code in [201, 200]
    return response.json()["id"]


def test_create_sea_shipment_no_discount(client: TestClient):
    client_id = create_mock_client(client)
    product_id = create_mock_product(client)
    port_id = create_mock_port(client)
    
    response = client.post(
        "/v1/sea-shipments/",
        headers=MOCK_HEADERS,
        json={
            "client_id": client_id,
            "product_id": product_id,
            "port_id": port_id,
            "quantity": 5, 
            "register_date": "2025-11-01",
            "delivery_date": "2025-11-15",
            "price": 2000.0,
            "fleet_number": "ABC1000Z",
            "guide_number": "SEA0000001"
        }
    )
    
    assert response.status_code == 201
    data = response.json()
    
    assert data["discount"] == 0.0
    assert data["final_price"] == 10000.0 
    

def test_create_sea_shipment_with_discount(client: TestClient):
    client_id = create_mock_client(client)
    product_id = create_mock_product(client)
    port_id = create_mock_port(client)

    response = client.post(
        "/v1/sea-shipments/",
        headers=MOCK_HEADERS,
        json={
            "client_id": client_id,
            "product_id": product_id,
            "port_id": port_id,
            "quantity": 15, 
            "register_date": "2025-11-05",
            "delivery_date": "2025-11-25",
            "price": 2000.0,
            "fleet_number": "XYZ9999A",
            "guide_number": "SEA0000002"
        }
    )
    
    assert response.status_code == 201
    data = response.json()
    
    assert data["discount"] == 900.0 
    assert data["final_price"] == 29100.0


def test_list_sea_shipments_filter_by_fleet_and_guide(client: TestClient):
    client_id = create_mock_client(client)
    product_id = create_mock_product(client)
    port_id = create_mock_port(client)

    fleet = "DAT1234B" 
    guide = "MYGUIDE003"
    
    response_create = client.post(
        "/v1/sea-shipments/",
        headers=MOCK_HEADERS,
        json={
            "client_id": client_id,
            "product_id": product_id,
            "port_id": port_id,
            "quantity": 1,
            "register_date": "2025-04-01",
            "delivery_date": "2025-04-30",
            "price": 100.0,
            "fleet_number": fleet, 
            "guide_number": guide 
        }
    )
    assert response_create.status_code == 201

    response_fleet = client.get(
        "/v1/sea-shipments/", 
        headers=MOCK_HEADERS, 
        params={"fleet_number": "DAT"}
    )
    assert response_fleet.status_code == 200
    assert any(item['fleet_number'] == fleet for item in response_fleet.json())
    
    response_guide = client.get(
        "/v1/sea-shipments/", 
        headers=MOCK_HEADERS, 
        params={"guide_number": "GUIDE0"}
    )
    assert response_guide.status_code == 200
    assert any(item['guide_number'] == guide for item in response_guide.json())


def test_list_sea_shipments_filter_by_date(client: TestClient):
    client_id = create_mock_client(client)
    product_id = create_mock_product(client)
    port_id = create_mock_port(client)

    test_date_str = "2025-05-20"
    response_create = client.post(
        "/v1/sea-shipments/",
        headers=MOCK_HEADERS,
        json={
            "client_id": client_id,
            "product_id": product_id,
            "port_id": port_id,
            "quantity": 1,
            "register_date": test_date_str,
            "delivery_date": "2025-06-05",
            "price": 100.0,
            "fleet_number": "FIL5000C",
            "guide_number": "SEA0000004" 
        }
    )
    assert response_create.status_code == 201 

    response_filter = client.get(
        "/v1/sea-shipments/", 
        headers=MOCK_HEADERS, 
        params={"date_from": test_date_str, "date_to": test_date_str}
    )
    
    assert response_filter.status_code == 200
    data_filtered = response_filter.json()
    assert any(item['guide_number'] == "SEA0000004" for item in data_filtered)