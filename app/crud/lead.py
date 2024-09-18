from sqlalchemy.orm import Session

from app.models.lead import Lead, Resume
from app.schemas.lead import LeadCreate, ResumeCreate

def get_leads(db: Session, skip: int = 0, limit: int = 10):
    return db.query(Lead).offset(skip).limit(limit).all()

def create_lead(db: Session, lead: LeadCreate):
    db_lead = Lead(**lead.model_dump())
    db.add(db_lead)
    db.commit()
    db.refresh(db_lead)
    return db_lead

def update_lead_state(db: Session, lead_id: int, state: str):
    db_lead = db.query(Lead).filter(Lead.id == lead_id).first()
    db_lead.state = state
    db.commit()
    db.refresh(db_lead)
    return db_lead

def create_resume(db: Session, resume: ResumeCreate):
    db_resume = Resume(**resume.model_dump())
    db.add(db_resume)
    db.commit()
    db.refresh(db_resume)
    return db_resume

def get_resume(db: Session, resume_id: int):
    return db.query(Resume).filter(Resume.id == resume_id).first()
