from sqlalchemy import (
    Column,
    Integer,
    Enum as SqlEnum,
    ForeignKey,
    DateTime,
    JSON,
    func,
)

from app.db.session import Base

from app.schemas.user_data_status import Status


class UserDataLogs(Base):
    __tablename__ = "user_data_logs"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("user.id", ondelete="SET NULL"), nullable=True)
    user_id_record = Column(Integer, nullable=False)
    change_type = Column(SqlEnum(Status), nullable=False)
    changed_fields = Column(JSON, nullable=True)
    timestamp = Column(DateTime, default=func.now(), nullable=False)
