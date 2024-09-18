from fastapi.responses import FileResponse
from pydantic import BaseModel
from typing import Optional
from app.models.lead import LeadStateEnum

class LeadBase(BaseModel):
    first_name: str
    last_name: str
    email: str
    resume_id: int


class LeadCreate(LeadBase):
    pass

class Lead(LeadBase):
    id: int
    state: LeadStateEnum

    class Config:
        from_attributes = True

class ResumeCreate(BaseModel):
    location: str

class ResumeUploadResponse(BaseModel):
    id: int
    