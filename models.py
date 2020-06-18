from sqlalchemy import Boolean, Column, ForeignKey, Numeric, Integer, String
from sqlalchemy.types import Date
from database import Base


class State(Base):
    __tablename__ = "state"

    id = Column(String, unique=True, index=True)
    state = Column(String, primary_key=True, index=True)
    confirmed = Column(Integer)
    active = Column(Integer)
    deaths = Column(Integer)
    recovered = Column(Integer)

