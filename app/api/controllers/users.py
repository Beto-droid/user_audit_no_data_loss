from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from app.schemas.user import User as UserSchema
from app.schemas.user import UserCreate as UserCreateSchema
from app.crud.user import (
    get_user,
    create_user,
    update_user_crud,
    query_user_by_parameters,
    delete_user_crud,
)
from app.db.session import get_db
from typing import List

router = APIRouter(
    prefix="/users",
)


@router.post("/", response_model=UserSchema)
def create_new_user(user: UserCreateSchema, db: Session = Depends(get_db)):
    return create_user(db=db, user=user)


@router.get("/", response_model=List[UserSchema])
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


@router.get("/{user_id}", response_model=UserSchema)
def get_user_by_id(user_id: int, db: Session = Depends(get_db)):
    db_user = get_user(db, user_id=user_id)
    if not db_user:
        raise HTTPException(
            status_code=404, detail="The user with this id does not exist in the system"
        )
    return db_user


@router.delete("/{user_id}")
def delete_user_by_id(user_id: int, db: Session = Depends(get_db)):
    db_user = get_user(db, user_id=user_id)
    if not db_user:
        raise HTTPException(
            status_code=404, detail="The user with this id does not exist in the system"
        )
    deleted_user = delete_user_crud(db=db, user_id=user_id)
    return JSONResponse(content=deleted_user, status_code=200)


@router.put("/{user_id}", response_model=UserSchema)
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

    changed_fields = {
        k: v for k, v in {"name": name, "email": email}.items() if v is not None
    }
    if not changed_fields:
        raise HTTPException(status_code=400, detail="No fields provided to update")

    return update_user_crud(db=db, user_id=user_id, changed_fields=changed_fields)
