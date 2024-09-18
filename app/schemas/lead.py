from pydantic import BaseModel

from app.models.lead import LeadStateEnum

class LeadBase(BaseModel):
    first_name: str
    last_name: str
    email: str
    resume_location: str

class LeadCreate(LeadBase):
    pass

class Lead(LeadBase):
    id: int
    state: LeadStateEnum

    class Config:
        from_attributes = True
