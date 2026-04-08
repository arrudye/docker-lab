from sqlalchemy import Boolean, Column, Integer, String

from src.core.database import Base


class Book(Base):
    __tablename__ = "books"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255), nullable=False)
    author = Column(String(255), nullable=False)
    genre = Column(String(100))
    year = Column(Integer)
    is_available = Column(Boolean, default=True)
