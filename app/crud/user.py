from enum import Enum
from functools import wraps

from sqlalchemy.orm import Session

from app.models import (
    User as UserModel,
    UserDataLogs as UserDataLogsModel,
    UserDataStatus as UserDataStatusModel,
    User,
)
from app.schemas import (
    User as UserSchema,
    UserCreate as UserCreateSchema,
    UserDataLogs as UserDataLogsSchema,
    UserDataStatus as UserDataStatusSchema,
)

from app.schemas.user_data_status import Status

from datetime import datetime

from typing import List, Optional, Type


def log_status_change(db: Session, user_id: int, status: Status):
    status_entry = UserDataStatusModel(user_id=user_id, status=status)
    db.add(status_entry)


def log_change(db: Session, user_id: int, change_type: Status, changed_fields: dict):
    log_entry = UserDataLogsModel(
        user_id=user_id,
        change_type=change_type,
        changed_fields=changed_fields,
    )
    db.add(log_entry)

def log_user_creation(func):
    """
    Decorator to log user creation and init the other tables (data_logs and data_status)
    :param func:
    :return:
    """

    @wraps(func)
    def wrapper(db: Session, *args, **kwargs):
        user = func(db, *args, **kwargs)
        status_entry = UserDataStatusModel(user_id=user.id, status=Status.CREATED)
        db.add(status_entry)

        log_entry = UserDataLogsModel(
            user_id=user.id,
            change_type=Status.CREATED,
            changed_fields={"name": user.name, "email": user.email},
        )
        db.add(log_entry)
        db.commit()
        return user

    return wrapper


def log_user_update(func):
    """
    Decorator to log the update of a user, so it also updates the other tables
    :param func:
    :return:
    """

    @wraps(func)
    def wrapper(db: Session, *args, **kwargs):
        user_id = kwargs.get("user_id")
        changed_fields = kwargs.get("changed_fields", {})

        # Now call the original fn.
        user = func(db, *args, **kwargs)
        status_entry = UserDataStatusModel(user_id=user_id, status=Status.UPDATED)
        db.add(status_entry)

        # Now add it to the log table.
        log_entry = UserDataLogsModel(
            user_id=user_id,
            change_type=Status.UPDATED,
            changed_fields=changed_fields,
        )
        db.add(log_entry)
        db.commit()
        return user

    return wrapper


def log_user_deletion(func):
    """
    Decorator when the user its deleted.
    :param func:
    :return:
    """

    @wraps(func)
    def wrapper(db: Session, *args, **kwargs):
        user_id = kwargs.get("user_id")
        changed_fields = kwargs.get("changed_fields", {})

        user = func(db, *args, **kwargs)

        status_entry = UserDataStatusModel(user_id=user_id, status=Status.DELETED)
        db.add(status_entry)

        log_entry = UserDataLogsModel(
            user_id=user_id,
            change_type=Status.DELETED,
            changed_fields=changed_fields,
        )
        db.add(log_entry)
        db.commit()
        return user

    return wrapper


def get_user(db: Session, user_id: int):
    return db.query(UserModel).filter(UserModel.id == user_id).first()


@log_user_creation
def create_user(db: Session, user: UserCreateSchema):
    db_item = UserModel(name=user.name, email=user.email)
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item


def query_user_by_parameters(
    db: Session,
    user_id: Optional[int] = None,
    name: Optional[str] = None,
    email: Optional[str] = None,
) -> list[Type[User]]:
    query = db.query(UserModel)
    if user_id is not None:
        query = query.filter(UserModel.id == user_id)
    if name is not None:
        query = query.filter(UserModel.name == name)
    if email is not None:
        query = query.filter(UserModel.email == email)

    return query.all()


@log_user_update
def update_user_crud(db: Session, user_id: int):
    """Update an existing user."""
    user = db.query(UserModel).filter(UserModel.id == user_id).first()

    for key, value in changed_fields.items():
        setattr(user, key, value)
    db.commit()
    db.refresh(user)
    return user
