from typing import List, Optional
from sqlalchemy.orm import Session
from src.models import Book
from src.repositories.base_repo import BaseRepository

class BookRepository(BaseRepository[Book]):
    def __init__(self, db: Session):
        super().__init__(Book, db)
    
    def search(self, 
               title: Optional[str] = None, 
               author: Optional[str] = None, 
               genre: Optional[str] = None) -> List[Book]:
        query = self.db.query(Book)
        
        if title:
            query = query.filter(Book.title.ilike(f"%{title}%"))
        if author:
            query = query.filter(Book.author.ilike(f"%{author}%"))
        if genre:
            query = query.filter(Book.genre.ilike(f"%{genre}%"))
        
        return query.all()