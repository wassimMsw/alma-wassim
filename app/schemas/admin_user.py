from pydantic import BaseModel

    
class AdminUser(BaseModel):
    email: str
    password: str