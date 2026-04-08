
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from src.core.database import get_db
from src.repositories.reader_repo import ReaderRepository
from src.schemas.reader import Reader, ReaderCreate, ReaderUpdate

router = APIRouter(prefix="/readers", tags=["readers"])

@router.get("/", response_model=list[Reader])
def get_readers(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    repo = ReaderRepository(db)
    return repo.get_all(skip=skip, limit=limit)

@router.get("/search", response_model=list[Reader])
def search_readers(
    name: str,
    db: Session = Depends(get_db)
):
    repo = ReaderRepository(db)
    return repo.search_by_name(name)

@router.get("/{reader_id}", response_model=Reader)
def get_reader(reader_id: int, db: Session = Depends(get_db)):
    repo = ReaderRepository(db)
    reader = repo.get(reader_id)
    if not reader:
        raise HTTPException(status_code=404, detail="Читатель не найден")
    return reader

@router.post("/", response_model=Reader, status_code=status.HTTP_201_CREATED)
def create_reader(reader: ReaderCreate, db: Session = Depends(get_db)):
    repo = ReaderRepository(db)

    existing = repo.get_by_email(reader.email)
    if existing:
        raise HTTPException(status_code=400, detail="Email уже используется")

    return repo.create(**reader.model_dump())

@router.put("/{reader_id}", response_model=Reader)
def update_reader(reader_id: int, reader: ReaderUpdate, db: Session = Depends(get_db)):
    repo = ReaderRepository(db)
    updated_reader = repo.update(reader_id, **reader.model_dump())
    if not updated_reader:
        raise HTTPException(status_code=404, detail="Читатель не найден")
    return updated_reader

@router.delete("/{reader_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_reader(reader_id: int, db: Session = Depends(get_db)):
    repo = ReaderRepository(db)
    deleted = repo.delete(reader_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Читатель не найден")
    return None
