import pytest


class TestLoansAPI:
    def test_create_loan(self, client):
        book = client.post("/books/", json={
            "title": "Книга для выдачи",
            "author": "Автор"
        }).json()
        
        reader = client.post("/readers/", json={
            "name": "Читатель",
            "email": "reader@loan.com"
        }).json()
        
        response = client.post("/loans/", json={
            "book_id": book["id"],
            "reader_id": reader["id"]
        })
        
        assert response.status_code == 201
        data = response.json()
        assert data["book_id"] == book["id"]
        assert data["reader_id"] == reader["id"]
        assert data["return_date"] is None
    
    def test_create_loan_unavailable_book(self, client):
        book = client.post("/books/", json={
            "title": "Недоступная книга",
            "author": "Автор"
        }).json()
        
        reader = client.post("/readers/", json={
            "name": "Читатель",
            "email": "reader2@loan.com"
        }).json()
        
        client.post("/loans/", json={
            "book_id": book["id"],
            "reader_id": reader["id"]
        })
        
        response = client.post("/loans/", json={
            "book_id": book["id"],
            "reader_id": reader["id"]
        })
        
        assert response.status_code == 400
        assert "недоступна" in response.json()["detail"]
    
    def test_create_loan_book_not_found(self, client, sample_reader_data):
        reader = client.post("/readers/", json=sample_reader_data).json()
        
        response = client.post("/loans/", json={
            "book_id": 99999,
            "reader_id": reader["id"]
        })
        
        assert response.status_code == 404
    
    def test_return_book(self, client):
        book = client.post("/books/", json={
            "title": "Книга для возврата",
            "author": "Автор"
        }).json()
        
        reader = client.post("/readers/", json={
            "name": "Читатель",
            "email": "return@test.com"
        }).json()

        loan = client.post("/loans/", json={
            "book_id": book["id"],
            "reader_id": reader["id"]
        }).json()
        
        response = client.post(f"/loans/{loan['id']}/return")
        
        assert response.status_code == 200
        data = response.json()
        assert data["return_date"] is not None
    
        updated_book = client.get(f"/books/{book['id']}").json()
        assert updated_book["is_available"] == True
    
    def test_return_nonexistent_loan(self, client):
        response = client.post("/loans/99999/return")
        
        assert response.status_code == 404
    
    def test_get_active_loans(self, client):
        response = client.get("/loans/active")
        
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)
    
    def test_get_reader_loans(self, client):
        reader = client.post("/readers/", json={
            "name": "Читатель для истории",
            "email": "history@test.com"
        }).json()
        
        response = client.get(f"/loans/reader/{reader['id']}")
        
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)
    
    def test_get_book_loans(self, client):
        book = client.post("/books/", json={
            "title": "Книга с историей",
            "author": "Автор"
        }).json()
        
        response = client.get(f"/loans/book/{book['id']}")
        
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)