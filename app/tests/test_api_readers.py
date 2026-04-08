import pytest


class TestReadersAPI:
    def test_create_reader(self, client, sample_reader_data):
        response = client.post("/readers/", json=sample_reader_data)
        
        assert response.status_code == 201
        data = response.json()
        assert data["name"] == sample_reader_data["name"]
        assert data["email"] == sample_reader_data["email"]
        assert "id" in data
    
    def test_create_reader_duplicate_email(self, client, sample_reader_data):
        client.post("/readers/", json=sample_reader_data)
        response = client.post("/readers/", json=sample_reader_data)
        
        assert response.status_code == 400
        assert "Email уже используется" in response.json()["detail"]
    
    def test_get_reader(self, client, sample_reader_data):
        create_response = client.post("/readers/", json=sample_reader_data)
        reader_id = create_response.json()["id"]
        
        response = client.get(f"/readers/{reader_id}")
        
        assert response.status_code == 200
        data = response.json()
        assert data["id"] == reader_id
        assert data["email"] == sample_reader_data["email"]
    
    def test_get_reader_not_found(self, client):
        response = client.get("/readers/99999")
        
        assert response.status_code == 404
    
    def test_get_all_readers(self, client):
        response = client.get("/readers/")
        
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)
    
    def test_search_readers(self, client):
        client.post("/readers/", json={"name": "Иван Петров", "email": "ivan@test.com"})
        client.post("/readers/", json={"name": "Петр Иванов", "email": "petr@test.com"})
        
        response = client.get("/readers/search?name=Иван")
        
        assert response.status_code == 200
        data = response.json()
        assert len(data) >= 1
        assert "Иван" in data[0]["name"]
    
    def test_update_reader(self, client, sample_reader_data):
        create_response = client.post("/readers/", json=sample_reader_data)
        reader_id = create_response.json()["id"]
        
        response = client.put(f"/readers/{reader_id}", json={"name": "Новое имя"})
        
        assert response.status_code == 200
        data = response.json()
        assert data["name"] == "Новое имя"
        assert data["email"] == sample_reader_data["email"]
    
    def test_delete_reader(self, client, sample_reader_data):
        create_response = client.post("/readers/", json=sample_reader_data)
        reader_id = create_response.json()["id"]
        
        response = client.delete(f"/readers/{reader_id}")
        
        assert response.status_code == 204
        
        get_response = client.get(f"/readers/{reader_id}")
        assert get_response.status_code == 404