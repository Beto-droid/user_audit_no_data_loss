from datetime import datetime
from enum import Enum

from pydantic import BaseModel, EmailStr, ConfigDict


class Status(Enum):
    CREATED = "created"
    UPDATED = "updated"
    DELETED = "deleted"


class UserDataStatus(BaseModel):
    id: int
    user_id: int
    status: Status
    modified_at: datetime

    model_config = ConfigDict(from_attributes=True)
