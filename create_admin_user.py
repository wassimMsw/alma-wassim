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

def main():
    db = SessionLocal()
    username = input("Enter username: ")
    password = input("Enter password: ")
    email = input("Enter email: ")
    hashed_password = get_password_hash(password)
    user = AdminUserInDB(username=username, hashed_password=hashed_password, email=email)
    try:
        user = create_admin_user(db, user)
        print(f"User created: {user.username}")
        print(f"Password: {password}")
    finally:
        db.close()

if __name__ == "__main__":
    main()
