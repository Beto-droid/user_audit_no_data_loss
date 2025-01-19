from pydantic import BaseModel, EmailStr



class UserCreate(BaseModel):
    name: str
    email: str

class User(BaseModel):
    id: int
    name: str
    email: str

    class Config:
        from_attributes = True
