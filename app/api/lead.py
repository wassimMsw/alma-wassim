from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

import app.crud.lead as lead_crud
from app.db.db import get_db
from app.models.lead import LeadStateEnum
from app.schemas.lead import LeadCreate, Lead

router = APIRouter()

@router.post("/leads/", response_model=Lead)
def create_lead(lead: LeadCreate, db: Session = Depends(get_db)):
    return lead_crud.create_lead(db=db, lead=lead)

@router.get("/leads/", response_model=list[Lead])
def read_leads(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    leads = lead_crud.get_leads(db, skip, limit)
    return leads

@router.put("/leads/{lead_id}/state", response_model=Lead)
def update_lead_state(lead_id: int, state: LeadStateEnum, db: Session = Depends(get_db)):
    return lead_crud.update_lead_state(db=db, lead_id=lead_id, state=state.value)