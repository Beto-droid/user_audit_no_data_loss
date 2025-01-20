from datetime import datetime
from typing import Optional, Dict

from pydantic import BaseModel, ConfigDict

from app.schemas.user_data_status import Status


class UserDataLogs(BaseModel):
    id: int
    user_id: int | None
    user_id_record: int
    change_type: Status
    changed_fields: Optional[Dict[str, Dict[str, str]]] = None
    timestamp: datetime

    model_config = ConfigDict(from_attributes=True)
