from sqlalchemy.orm import Session

from app.crud.user import get_user_by_name, get_user_by_email
from app.models import (
    UserDataLogs as UserDataLogsModel,
)


from typing import Optional, Type


def query_audit_by_parameters(
    db: Session,
    logs_id: int | None = None,
    user_id: Optional[int] = None,
    name: Optional[str] = None,
    email: Optional[str] = None,
) -> list[Type[UserDataLogsModel]]:
    query = db.query(UserDataLogsModel)
    if logs_id is not None:
        query = query.filter(UserDataLogsModel.id == logs_id)
    if user_id is not None:
        query = query.filter(UserDataLogsModel.user_id == user_id)
    if name is not None:
        matching_users = get_user_by_name(db, name=name)
        if not matching_users:
            return []
        user_ids = [user.id for user in matching_users]
        query = query.filter(UserDataLogsModel.user_id.in_(user_ids))
    if email is not None:
        matching_users = get_user_by_email(db, email=email)
        if not matching_users:
            return []
        user_ids = [user.id for user in matching_users]
        query = query.filter(UserDataLogsModel.user_id.in_(user_ids))

    return query.all()


def get_user_audit(db: Session, audit_id: int):
    return db.query(UserDataLogsModel).filter(UserDataLogsModel.id == audit_id).first()
