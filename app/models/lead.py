from sqlalchemy import Column, ForeignKey, Integer, String

from app.db.db import Base

from enum import Enum

class LeadStateEnum(Enum):
    PENDING = "PENDING"
    REACHED_OUT = "REACHED_OUT"


class LeadState(Base):
    __tablename__ = "lead_states"

    name = Column(String(255), primary_key=True)


class Lead(Base):
    __tablename__ = "leads"

    id = Column(Integer, primary_key=True)
    first_name = Column(String(255), index=True)
    last_name = Column(String(255), index=True)
    email = Column(String(255), index=True)
    resume_location = Column(String(255))
    state = Column(String(255), ForeignKey("lead_states.name"), default=LeadStateEnum.PENDING.value)
