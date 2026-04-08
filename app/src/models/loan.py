from datetime import date

from sqlalchemy import Column, Date, ForeignKey, Integer
from sqlalchemy.orm import relationship

from src.core.database import Base


class Loan(Base):
    __tablename__ = "loans"

    id = Column(Integer, primary_key=True, index=True)
    book_id = Column(Integer, ForeignKey("books.id", ondelete="CASCADE"))
    reader_id = Column(Integer, ForeignKey("readers.id", ondelete="CASCADE"))
    loan_date = Column(Date, default=date.today)
    return_date = Column(Date, nullable=True)

    book = relationship("Book")
    reader = relationship("Reader")
