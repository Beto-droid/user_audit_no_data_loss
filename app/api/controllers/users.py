from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.schemas.user import User as UserSchema
from app.schemas.user import UserCreate as UserCreateSchema
from app.crud.user import (
    get_user,
    create_user,
    update_user_crud,
    query_user_by_parameters,
)
from app.db.session import get_db
from typing import Annotated, List

router = APIRouter()


@router.post("/users/", response_model=UserSchema)
def create_new_user(user: UserCreateSchema, db: Session = Depends(get_db)):
    return create_user(db=db, user=user)


@router.get("/users/", response_model=List[UserSchema])
def query_users_by_parameters(
    user_id: int | None = None,
    name: str | None = None,
    email: str | None = None,
    db: Session = Depends(get_db),
):
    users = query_user_by_parameters(db, user_id=user_id, name=name, email=email)

    if not users:
        raise HTTPException(
            status_code=404, detail="No users found matching the given parameters."
        )
    return users


@router.get("/users/{user_id}", response_model=UserSchema)
def get_user_by_id(user_id: int, db: Session = Depends(get_db)):
    db_user = get_user(db, user_id=user_id)
    if not db_user:
        raise HTTPException(
            status_code=404, detail="The user with this id does not exist in the system"
        )
    return db_user


@router.put("/users/{user_id}")
def update_user(
    user_id: int,
    name: str | None = None,
    email: str | None = None,
    db: Session = Depends(get_db),
):
    db_user = get_user(db, user_id=user_id)
    if not db_user:
        raise HTTPException(
            status_code=404, detail="The user with this id does not exist in the system"
        )
    return update_user_crud(user_id=user_id, name=name, email=email)
