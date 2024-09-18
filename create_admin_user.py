import random
import string
from sqlalchemy.orm import Session
from app.crud.admin_user import create_admin_user
from app.db.db import SessionLocal
from app.auth.auth import get_password_hash
from app.schemas.admin_user import AdminUserInDB

def generate_random_password(length=12):
    characters = string.ascii_letters + string.digits + string.punctuation
    return ''.join(random.choice(characters) for _ in range(length))

def create_user(username: str, db: Session):
    password = generate_random_password()
    hashed_password = get_password_hash(password)
    user = AdminUserInDB(username=username, hashed_password=hashed_password)
    user = create_admin_user(db,user)
    return user, password

def main():
    db = SessionLocal()
    try:
        username = "new_user"
        user, password = create_user(username, db)
        print(f"User created: {user.username}")
        print(f"Password: {password}")
    finally:
        db.close()

if __name__ == "__main__":
    main()
