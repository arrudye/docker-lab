from pydantic import BaseModel, ConfigDict
from datetime import date
from typing import Optional

class LoanBase(BaseModel):
    book_id: int
    reader_id: int

class LoanCreate(LoanBase):
    pass

class LoanReturn(BaseModel):
    return_date: Optional[date] = None

class Loan(LoanBase):
    id: int
    loan_date: date
    return_date: Optional[date] = None
    
    model_config = ConfigDict(from_attributes=True)