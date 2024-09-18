import os
from typing import Annotated
import uuid
from fastapi import APIRouter, Depends, HTTPException, UploadFile
from fastapi.responses import FileResponse
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session

from app.auth.auth import get_current_active_user
import app.crud.lead as lead_crud
from app.db.db import get_db
from app.models.lead import LeadStateEnum
from app.schemas.admin_user import AdminUser
from app.schemas.lead import LeadCreate, Lead, ResumeCreate, ResumeUploadResponse

router = APIRouter()


UPLOAD_DIRECTORY = os.path.join(os.getcwd(), "uploads")

@router.post("/upload/resume", response_model=ResumeUploadResponse)
async def upload_resume(resume: UploadFile, db: Session = Depends(get_db)):
    # Ensure the upload directory exists
    os.makedirs(UPLOAD_DIRECTORY, exist_ok=True)
    
    # Save the uploaded file to the temporary directory with a unique identifier
    unique_filename = f"{uuid.uuid4()}_{resume.filename}"
    file_location = os.path.join(UPLOAD_DIRECTORY, unique_filename)
    try:
        with open(file_location, "wb+") as file_object:
            file_object.write(resume.file.read())
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Could not save file: {str(e)}")
    
    # Create a new resume entry in the database
    resume_create = ResumeCreate(location=file_location)
    db_resume = lead_crud.create_resume(db=db, resume=resume_create)
    
    return ResumeUploadResponse(id=db_resume.id)


@router.post("/leads/", response_model=Lead)
def create_lead(lead: LeadCreate, db: Session = Depends(get_db)):
    return lead_crud.create_lead(db=db, lead=lead)

@router.get("/leads/", response_model=list[Lead])
def read_leads(_ :  Annotated[AdminUser, Depends(get_current_active_user)], skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    leads = lead_crud.get_leads(db, skip, limit)
    return leads

@router.put("/leads/{lead_id}/state", response_model=Lead)
def update_lead_state(_ :  Annotated[AdminUser, Depends(get_current_active_user)],lead_id: int, state: LeadStateEnum, db: Session = Depends(get_db)):
    return lead_crud.update_lead_state(db=db, lead_id=lead_id, state=state.value)

@router.get("/resume/{resume_id}", response_class=FileResponse)
async def download_resume(resume_id: int, db: Session = Depends(get_db)):
    # Fetch the resume from the database
    resume = lead_crud.get_resume(db=db, resume_id=resume_id)
    if not resume:
        raise HTTPException(status_code=404, detail="Resume not found")
    
    # Check if the file exists
    if not os.path.exists(resume.location):
        raise HTTPException(status_code=404, detail="Resume file not found")
    
    # Return the file
    return resume.location
