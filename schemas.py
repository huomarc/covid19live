from datetime import date
from pydantic import BaseModel


class Record(BaseModel):
    id: str
    state: str
    confirmed: int
    active: int
    deaths : int
    recovered : int

    class Config:
        orm_mode = True