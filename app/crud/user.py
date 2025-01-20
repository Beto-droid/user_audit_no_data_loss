from functools import wraps

from sqlalchemy import func as sqlfunc
from sqlalchemy.orm import Session

from app.models import (
    User as UserModel,
    UserDataLogs as UserDataLogsModel,
    UserDataStatus as UserDataStatusModel,
)
from app.schemas import (
    UserCreate as UserCreateSchema,
)

from app.schemas.user_data_status import Status

from typing import Optional, Type


def log_status_change(db: Session, user_id: int, status: Status):
    status_entry = (
        db.query(UserDataStatusModel)
        .filter(UserDataStatusModel.user_id == user_id)
        .first()
    )

    if status_entry:
        status_entry.status = status
        status_entry.modified_at = sqlfunc.now()
    else:
        status_entry = UserDataStatusModel(user_id=user_id, status=status)
        db.add(status_entry)
    db.commit()


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
        log_status_change(db, user_id=user.id, status=Status.CREATED)

        log_change(
            db,
            user_id=user.id,
            change_type=Status.CREATED,
            changed_fields={
                "old": {},
                "new": {"name": user.name, "email": user.email},
            },
        )
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

        existing_user = db.query(UserModel).filter(UserModel.id == user_id).first()
        old_data = {"name": existing_user.name, "email": existing_user.email}

        user = func(db, *args, **kwargs)

        log_status_change(db, user_id=user.id, status=Status.UPDATED)

        log_change(
            db,
            user_id=user_id,
            change_type=Status.UPDATED,
            changed_fields={
                "old": old_data,
                "new": {
                    k: v
                    for k, v in {"name": user.name, "email": user.email}.items()
                    if v is not None
                },
            },
        )

        db.commit()
        return user

    return wrapper


def log_user_delete(func):
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

        log_status_change(db, user_id=user.id, status=Status.DELETED)
        log_change(
            db,
            user_id=user_id,
            change_type=Status.DELETED,
            changed_fields=changed_fields,
        )
        db.commit()
        return user

    return wrapper


def get_user(db: Session, user_id: int):
    return db.query(UserModel).filter(UserModel.id == user_id).first()


def get_user_by_name(db: Session, name: str):
    return db.query(UserModel).filter(UserModel.name == name).all()


def get_user_by_email(db: Session, email: str):
    return db.query(UserModel).filter(UserModel.email == email).all()


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
) -> list[Type[UserModel]]:
    query = db.query(UserModel)
    if user_id is not None:
        query = query.filter(UserModel.id == user_id)
    if name is not None:
        query = query.filter(UserModel.name == name)
    if email is not None:
        query = query.filter(UserModel.email == email)

    return query.all()


@log_user_update
def update_user_crud(db: Session, user_id: int, changed_fields: dict):
    user = get_user(db, user_id=user_id)
    for key, value in changed_fields.items():
        setattr(user, key, value)
    db.commit()
    db.refresh(user)
    return user


@log_user_delete
def delete_user_crud(db: Session, user_id: int):
    user = get_user(db, user_id=user_id)
    db.delete(user)
    db.commit()
    return user
