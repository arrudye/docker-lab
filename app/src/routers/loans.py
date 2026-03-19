from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from src.core.database import get_db
from src.schemas.loan import Loan, LoanCreate, LoanReturn
from src.repositories.loan_repo import LoanRepository
from src.repositories.book_repo import BookRepository
from src.repositories.reader_repo import ReaderRepository

router = APIRouter(prefix="/loans", tags=["loans"])

@router.get("/", response_model=List[Loan])
def get_loans(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    repo = LoanRepository(db)
    return repo.get_all(skip=skip, limit=limit)

@router.get("/active", response_model=List[Loan])
def get_active_loans(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    repo = LoanRepository(db)
    return repo.get_active_loans(skip=skip, limit=limit)

@router.get("/reader/{reader_id}", response_model=List[Loan])
def get_reader_loans(reader_id: int, db: Session = Depends(get_db)):
    repo = LoanRepository(db)
    return repo.get_reader_loans(reader_id)

@router.get("/book/{book_id}", response_model=List[Loan])
def get_book_loans(book_id: int, db: Session = Depends(get_db)):
    repo = LoanRepository(db)
    return repo.get_book_loans(book_id)

@router.post("/", response_model=Loan, status_code=status.HTTP_201_CREATED)
def create_loan(loan: LoanCreate, db: Session = Depends(get_db)):
    book_repo = BookRepository(db)
    reader_repo = ReaderRepository(db)
    
    book = book_repo.get(loan.book_id)
    if not book:
        raise HTTPException(status_code=404, detail="Книга не найдена")
    
    if not book.is_available:
        raise HTTPException(status_code=400, detail="Книга недоступна")
    
    reader = reader_repo.get(loan.reader_id)
    if not reader:
        raise HTTPException(status_code=404, detail="Читатель не найден")
    
    loan_repo = LoanRepository(db)
    new_loan = loan_repo.create_loan(loan.book_id, loan.reader_id)
    
    if not new_loan:
        raise HTTPException(status_code=400, detail="Не удалось создать выдачу")
    
    return new_loan

@router.post("/{loan_id}/return", response_model=Loan)
def return_book(loan_id: int, db: Session = Depends(get_db)):
    repo = LoanRepository(db)
    returned_loan = repo.return_book(loan_id)
    
    if not returned_loan:
        raise HTTPException(status_code=404, detail="Выдача не найдена либо книга уже возвращена")
    
    return returned_loan