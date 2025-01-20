from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.schemas.user_data_logs import UserDataLogs as UserDataLogsSchema
from app.crud.audit import query_audit_by_parameters, get_user_audit
from app.db.session import get_db
from typing import List

router = APIRouter(
    prefix="/audit",
)


@router.get("/", response_model=List[UserDataLogsSchema])
def query_users_by_parameters(
    logs_id: int | None = None,
    user_id: int | None = None,
    name: str | None = None,
    email: str | None = None,
    db: Session = Depends(get_db),
):
    users_audit_list = query_audit_by_parameters(
        db, logs_id=logs_id, user_id=user_id, name=name, email=email
    )

    if not users_audit_list:
        raise HTTPException(
            status_code=404,
            detail="No audit for user found matching the given parameters.",
        )
    return users_audit_list


@router.get("/{audit_id}", response_model=UserDataLogsSchema)
def get_user_by_id(audit_id: int, db: Session = Depends(get_db)):
    user_audit = get_user_audit(db, audit_id=audit_id)
    if not user_audit:
        raise HTTPException(
            status_code=404, detail="The user with this id does not exist in the system"
        )
    return user_audit
