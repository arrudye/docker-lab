import pytest


class TestBooksAPI:
    def test_create_book(self, client, sample_book_data):
        response = client.post("/books/", json=sample_book_data)
        
        assert response.status_code == 201
        data = response.json()
        assert data["title"] == sample_book_data["title"]
        assert data["author"] == sample_book_data["author"]
        assert data["is_available"] == True
        assert "id" in data
    
    def test_create_book_missing_fields(self, client):
        response = client.post("/books/", json={"title": "Только название"})
        
        assert response.status_code == 422
    
    def test_get_book(self, client, sample_book_data):
        create_response = client.post("/books/", json=sample_book_data)
        book_id = create_response.json()["id"]
        
        response = client.get(f"/books/{book_id}")
        
        assert response.status_code == 200
        data = response.json()
        assert data["id"] == book_id
        assert data["title"] == sample_book_data["title"]
    
    def test_get_book_not_found(self, client):
        response = client.get("/books/99999")
        
        assert response.status_code == 404
        assert "не найдена" in response.json()["detail"]
    
    def test_get_all_books(self, client, sample_book_data):
        client.post("/books/", json=sample_book_data)
        client.post("/books/", json={
            "title": "Другая книга",
            "author": "Другой автор"
        })
        
        response = client.get("/books/")
        
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)
        assert len(data) >= 2
    
    def test_get_books_with_pagination(self, client):
        response = client.get("/books/?skip=0&limit=5")
        
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)
    
    def test_update_book(self, client, sample_book_data):
        create_response = client.post("/books/", json=sample_book_data)
        book_id = create_response.json()["id"]
        
        update_data = {"title": "Обновленное название"}
        response = client.put(f"/books/{book_id}", json=update_data)
        
        assert response.status_code == 200
        data = response.json()
        assert data["title"] == "Обновленное название"
        assert data["author"] == sample_book_data["author"]
    
    def test_update_book_not_found(self, client):
        response = client.put("/books/99999", json={"title": "Новое"})
        
        assert response.status_code == 404
    
    def test_delete_book(self, client, sample_book_data):
        create_response = client.post("/books/", json=sample_book_data)
        book_id = create_response.json()["id"]
        
        response = client.delete(f"/books/{book_id}")
        
        assert response.status_code == 204
        
        get_response = client.get(f"/books/{book_id}")
        assert get_response.status_code == 404
    
    def test_delete_book_not_found(self, client):
        response = client.delete("/books/99999")
        
        assert response.status_code == 404