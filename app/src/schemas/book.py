
from pydantic import BaseModel, ConfigDict


class BookBase(BaseModel):
    title: str
    author: str
    genre: str | None = None
    year: int | None = None

class BookCreate(BookBase):
    pass

class BookUpdate(BaseModel):
    title: str | None = None
    author: str | None = None
    genre: str | None = None
    year: int | None = None
    is_available: bool | None = None

class BookResponse(BookBase):
    id: int
    is_available: bool

    model_config = ConfigDict(from_attributes=True)
