from datetime import datetime
from typing import Optional, Dict

from pydantic import BaseModel

from app.schemas.user_data_status import Status


class UserDataLogs(BaseModel):
    id: int
    user_id: int
    user_data_status_id: int
    change_type: Status
    changed_fields: Optional[Dict[str, Dict[str, str]]] = None
    modified_at: datetime

    class Config:
        from_attributes = True
