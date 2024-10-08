from pydantic import BaseModel


class AdminUser(BaseModel):
    username: str
    email: str
    disabled: bool | None = None


class AdminUserInDB(AdminUser):
    hashed_password: str