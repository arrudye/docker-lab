import pytest
from src.repositories.book_repo import BookRepository
from src.repositories.reader_repo import ReaderRepository
from src.repositories.loan_repo import LoanRepository
from src.models import Book, Reader


class TestBookRepository:
    def test_create_book(self, db_session):
        repo = BookRepository(db_session)
        book = repo.create(
            title="Тестовая книга",
            author="Тестовый автор"
        )
        
        assert book.id is not None
        assert book.title == "Тестовая книга"
    
    def test_get_book(self, db_session):
        repo = BookRepository(db_session)
        created = repo.create(title="Книга", author="Автор")
        
        fetched = repo.get(created.id)
        assert fetched is not None
        assert fetched.id == created.id
    
    def test_get_all_books(self, db_session):
        repo = BookRepository(db_session)
        repo.create(title="Книга 1", author="Автор 1")
        repo.create(title="Книга 2", author="Автор 2")
        
        books = repo.get_all()
        assert len(books) >= 2
    
    def test_update_book(self, db_session):
        repo = BookRepository(db_session)
        book = repo.create(title="Старое название", author="Автор")
        
        updated = repo.update(book.id, title="Новое название")
        assert updated.title == "Новое название"
    
    def test_delete_book(self, db_session):
        repo = BookRepository(db_session)
        book = repo.create(title="Книга", author="Автор")
        
        deleted = repo.delete(book.id)
        assert deleted == True
        
        fetched = repo.get(book.id)
        assert fetched is None
    
    def test_search_books(self, db_session):
        repo = BookRepository(db_session)
        repo.create(title="Война и мир", author="Толстой")
        repo.create(title="Преступление и наказание", author="Достоевский")
        
        results = repo.search(title="Война")
        assert len(results) == 1
        assert results[0].title == "Война и мир"
        
        results = repo.search(author="Достоевский")
        assert len(results) == 1
        assert results[0].author == "Достоевский"


class TestReaderRepository:
    def test_create_reader(self, db_session):
        repo = ReaderRepository(db_session)
        reader = repo.create(
            name="Тестовый читатель",
            email="test@example.com"
        )
        
        assert reader.id is not None
        assert reader.email == "test@example.com"
    
    def test_get_by_email(self, db_session):
        repo = ReaderRepository(db_session)
        repo.create(name="Иван", email="ivan@example.com")
        
        reader = repo.get_by_email("ivan@example.com")
        assert reader is not None
        assert reader.name == "Иван"
    
    def test_search_by_name(self, db_session):
        repo = ReaderRepository(db_session)
        repo.create(name="Иван Петров", email="ivan@example.com")
        repo.create(name="Петр Иванов", email="petr@example.com")
        
        results = repo.search_by_name("Иван")
        assert len(results) == 2
        assert "Иван" in results[0].name or "Иван" in results[1].name
        
        results = repo.search_by_name("Иван Петров")
        assert len(results) == 1
        assert results[0].name == "Иван Петров"


class TestLoanRepository:
    def test_create_loan(self, db_session):
        book_repo = BookRepository(db_session)
        reader_repo = ReaderRepository(db_session)
        loan_repo = LoanRepository(db_session)
        
        book = book_repo.create(title="Книга", author="Автор")
        reader = reader_repo.create(name="Читатель", email="reader@example.com")
        
        loan = loan_repo.create_loan(book.id, reader.id)
        
        assert loan is not None
        assert loan.book_id == book.id
        assert loan.reader_id == reader.id
        assert loan.return_date is None
        
        updated_book = book_repo.get(book.id)
        assert updated_book.is_available == False
    
    def test_create_loan_unavailable_book(self, db_session):
        book_repo = BookRepository(db_session)
        reader_repo = ReaderRepository(db_session)
        loan_repo = LoanRepository(db_session)
        
        book = book_repo.create(title="Книга", author="Автор", is_available=False)
        reader = reader_repo.create(name="Читатель", email="reader@example.com")
        
        loan = loan_repo.create_loan(book.id, reader.id)
        assert loan is None
    
    def test_return_book(self, db_session):
        book_repo = BookRepository(db_session)
        reader_repo = ReaderRepository(db_session)
        loan_repo = LoanRepository(db_session)
        
        book = book_repo.create(title="Книга", author="Автор")
        reader = reader_repo.create(name="Читатель", email="reader@example.com")
        
        loan = loan_repo.create_loan(book.id, reader.id)
        assert loan is not None
        
        returned = loan_repo.return_book(loan.id)
        assert returned is not None
        assert returned.return_date is not None
        
        updated_book = book_repo.get(book.id)
        assert updated_book.is_available == True
    
    def test_get_active_loans(self, db_session):
        book_repo = BookRepository(db_session)
        reader_repo = ReaderRepository(db_session)
        loan_repo = LoanRepository(db_session)
        
        book = book_repo.create(title="Книга", author="Автор")
        reader = reader_repo.create(name="Читатель", email="reader@example.com")
        
        loan_repo.create_loan(book.id, reader.id)
        
        active = loan_repo.get_active_loans()
        assert len(active) == 1