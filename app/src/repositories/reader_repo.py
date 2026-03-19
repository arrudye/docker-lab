from typing import List, Optional
from sqlalchemy.orm import Session
from src.models import Reader, Loan
from src.repositories.base_repo import BaseRepository

class ReaderRepository(BaseRepository[Reader]):
    def __init__(self, db: Session):
        super().__init__(Reader, db)
    
    def get_by_email(self, email: str) -> Optional[Reader]:
        return self.db.query(Reader).filter(Reader.email == email).first()
    
    def search_by_name(self, name: str) -> List[Reader]:
        return self.db.query(Reader).filter(Reader.name.ilike(f"%{name}%")).all()
    
    def get_active_loans(self, reader_id: int) -> List:
        return self.db.query(Loan).filter(
            Loan.reader_id == reader_id,
            Loan.return_date.is_(None)
        ).all()