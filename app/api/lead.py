import os
import smtplib
import random
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from typing import Annotated
import uuid
from fastapi import APIRouter, Depends, HTTPException, UploadFile, BackgroundTasks
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session

from app.auth.auth import get_current_active_user
from app.crud.admin_user import get_admin_users
import app.crud.lead as lead_crud
from app.db.db import get_db
from app.models.lead import LeadStateEnum
from app.schemas.admin_user import AdminUser
from app.schemas.lead import LeadCreate, Lead, ResumeCreate, ResumeUploadResponse
from app.core.config import settings
router = APIRouter()

UPLOAD_DIRECTORY = os.path.join(os.getcwd(), "uploads")

# Email configuration
def send_email(to_email: str, subject: str, body: str):
    msg = MIMEMultipart()
    msg['From'] = settings.from_email
    msg['To'] = to_email
    msg['Subject'] = subject

    msg.attach(MIMEText(body, 'plain'))

    try:
        with smtplib.SMTP(settings.smtp_server, settings.smtp_port) as server:
            server.starttls()
            server.login(settings.smtp_username, settings.smtp_password)
            server.sendmail(settings.from_email, to_email, msg.as_string())
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Could not send email: {str(e)}")
        

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
def create_lead(lead: LeadCreate, db: Session = Depends(get_db), background_tasks: BackgroundTasks = BackgroundTasks()):
    new_lead = lead_crud.create_lead(db=db, lead=lead)
    
    # Fetch the lead creator's email
    lead_creator_email = new_lead.email
    
    # Fetch a random admin user's email
    admin_users = get_admin_users(db)
    if not admin_users:
        raise HTTPException(status_code=500, detail="No admin users found")
    random_admin_email = random.choice(admin_users).email
    
    # Send emails as background tasks
    subject = "New Lead Created"
    body = f"A new lead has been created with ID: {new_lead.id}"
    background_tasks.add_task(send_email, lead_creator_email, subject, body)
    background_tasks.add_task(send_email, random_admin_email, subject, body)
    
    return new_lead

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
