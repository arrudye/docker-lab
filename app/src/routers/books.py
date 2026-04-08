
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from src.core.database import get_db
from src.repositories.book_repo import BookRepository
from src.schemas.book import BookCreate, BookResponse, BookUpdate

router = APIRouter(prefix="/books", tags=["books"])

@router.post("/", response_model=BookResponse, status_code=201)
def create_book(
    book_data: BookCreate,
    db: Session = Depends(get_db)
):
    repo = BookRepository(db)
    new_book = repo.create(**book_data.model_dump())
    return new_book

@router.get("/{book_id}", response_model=BookResponse)
def get_book(
    book_id: int,
    db: Session = Depends(get_db)
):
    repo = BookRepository(db)
    book = repo.get(book_id)
    if not book:
        raise HTTPException(status_code=404, detail="Книга не найдена")
    return book

@router.get("/", response_model=list[BookResponse])
def get_books(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    repo = BookRepository(db)
    books = repo.get_all(skip=skip, limit=limit)
    return books

@router.put("/{book_id}", response_model=BookResponse)
def update_book(
    book_id: int,
    book_data: BookUpdate,
    db: Session = Depends(get_db)
):
    repo = BookRepository(db)
    updated_book = repo.update(book_id, **book_data.model_dump(exclude_unset=True))
    if not updated_book:
        raise HTTPException(status_code=404, detail="Книга не найдена")
    return updated_book

@router.delete("/{book_id}", status_code=204)
def delete_book(
    book_id: int,
    db: Session = Depends(get_db)
):
    repo = BookRepository(db)
    deleted = repo.delete(book_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Книга не найдена")
    return None
