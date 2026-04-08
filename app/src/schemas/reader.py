
from pydantic import BaseModel, ConfigDict, EmailStr


class ReaderBase(BaseModel):
    name: str
    email: EmailStr

class ReaderCreate(ReaderBase):
    pass

class ReaderUpdate(BaseModel):
    name: str | None = None
    email: EmailStr | None = None

class Reader(ReaderBase):
    id: int

    model_config = ConfigDict(from_attributes=True)
