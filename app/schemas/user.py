from pydantic import BaseModel, EmailStr, ConfigDict


class UserCreate(BaseModel):
    name: str
    email: str


class UserUpdate(BaseModel):
    name: str
    email: str


class User(BaseModel):
    id: int
    name: str
    email: str

    model_config = ConfigDict(from_attributes=True)
