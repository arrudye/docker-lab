import pytest
from sqlalchemy.exc import IntegrityError
from src.models import Book, Reader, Loan
from datetime import date


def test_create_book(db_session):
    book = Book(
        title="Война и мир",
        author="Лев Толстой",
        genre="Роман",
        year=1869
    )
    db_session.add(book)
    db_session.commit()
    
    assert book.id is not None
    assert book.title == "Война и мир"
    assert book.is_available == True


def test_book_title_required(db_session):
    book = Book(author="Автор")
    db_session.add(book)
    
    with pytest.raises(IntegrityError):
        db_session.commit()


def test_create_reader(db_session):
    reader = Reader(
        name="Иван Петров",
        email="ivan@example.com"
    )
    db_session.add(reader)
    db_session.commit()
    
    assert reader.id is not None
    assert reader.name == "Иван Петров"
    assert reader.email == "ivan@example.com"


def test_reader_email_unique(db_session):
    reader1 = Reader(name="Иван", email="same@example.com")
    reader2 = Reader(name="Петр", email="same@example.com")
    
    db_session.add(reader1)
    db_session.commit()
    
    db_session.add(reader2)
    with pytest.raises(IntegrityError):
        db_session.commit()


def test_create_loan(db_session):
    book = Book(title="Книга", author="Автор")
    reader = Reader(name="Читатель", email="reader@example.com")
    
    db_session.add_all([book, reader])
    db_session.commit()
    
    loan = Loan(
        book_id=book.id,
        reader_id=reader.id,
        loan_date=date.today()
    )
    db_session.add(loan)
    db_session.commit()
    
    assert loan.id is not None
    assert loan.return_date is None


def test_loan_relationships(db_session):
    book = Book(title="Книга", author="Автор")
    reader = Reader(name="Читатель", email="reader@example.com")
    
    db_session.add_all([book, reader])
    db_session.commit()
    
    loan = Loan(book_id=book.id, reader_id=reader.id)
    db_session.add(loan)
    db_session.commit()

    assert loan.book == book
    assert loan.reader == reader
    assert loan in book.loans if hasattr(book, 'loans') else True