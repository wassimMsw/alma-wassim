from sqlalchemy.orm import Session

from app.models.lead import Lead
from app.schemas.lead import LeadCreate

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