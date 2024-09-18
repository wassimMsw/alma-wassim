from sqlalchemy.orm import Session

from app.models.admin_user import AdminUser as AdminUserModel
from app.schemas.admin_user import AdminUserInDB

def get_admin_user(db: Session, username: str):
    return db.query(AdminUserModel).filter(AdminUserModel.username == username).first()

def create_admin_user(db: Session, admin_user: AdminUserInDB):
    db_admin_user = AdminUserModel(**admin_user.model_dump())
    db.add(db_admin_user)
    db.commit()
    db.refresh(db_admin_user)
    return db_admin_user

def get_admin_users(db: Session):
    return db.query(AdminUserModel).filter(AdminUserModel.disabled == False).all()
