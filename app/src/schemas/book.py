from pydantic import BaseModel, ConfigDict, Field
from typing import Optional

class BookBase(BaseModel):
    title: str
    author: str
    genre: Optional[str] = None
    year: Optional[int] = None

class BookCreate(BookBase):
    pass

class BookUpdate(BaseModel):
    title: Optional[str] = None
    author: Optional[str] = None
    genre: Optional[str] = None
    year: Optional[int] = None
    is_available: Optional[bool] = None

class BookResponse(BookBase):
    id: int
    is_available: bool
    
    model_config = ConfigDict(from_attributes=True)