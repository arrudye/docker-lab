from datetime import date

from sqlalchemy.orm import Session

from src.models import Book, Loan
from src.repositories.base_repo import BaseRepository


class LoanRepository(BaseRepository[Loan]):
    def __init__(self, db: Session):
        super().__init__(Loan, db)

    def create_loan(self, book_id: int, reader_id: int) -> Loan | None:
        book = self.db.query(Book).filter(Book.id == book_id).first()
        if not book or not book.is_available:
            return None

        loan = Loan(
            book_id=book_id,
            reader_id=reader_id,
            loan_date=date.today()
        )

        book.is_available = False

        self.db.add(loan)
        self.db.commit()
        self.db.refresh(loan)
        return loan

    def return_book(self, loan_id: int) -> Loan | None:
        loan = self.get(loan_id)
        if not loan or loan.return_date is not None:
            return None

        loan.return_date = date.today()

        book = self.db.query(Book).filter(Book.id == loan.book_id).first()
        if book:
            book.is_available = True

        self.db.commit()
        self.db.refresh(loan)
        return loan

    def get_active_loans(self, skip: int = 0, limit: int = 100) -> list[Loan]:
        return self.db.query(Loan).filter(Loan.return_date.is_(None)).offset(skip).limit(limit).all()

    def get_reader_loans(self, reader_id: int) -> list[Loan]:
        return self.db.query(Loan).filter(Loan.reader_id == reader_id).all()

    def get_book_loans(self, book_id: int) -> list[Loan]:
        return self.db.query(Loan).filter(Loan.book_id == book_id).all()
