from datetime import date

from pydantic import BaseModel, ConfigDict


class LoanBase(BaseModel):
    book_id: int
    reader_id: int

class LoanCreate(LoanBase):
    pass

class LoanReturn(BaseModel):
    return_date: date | None = None

class Loan(LoanBase):
    id: int
    loan_date: date
    return_date: date | None = None

    model_config = ConfigDict(from_attributes=True)
