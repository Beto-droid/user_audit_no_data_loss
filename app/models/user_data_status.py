from sqlalchemy import Column, Integer, ForeignKey, Enum as SqlEnum, DateTime, func

from app.db.session import Base

from app.schemas.user_data_status import Status


class UserDataStatus(Base):
    """
    Current status of the user with last time that had a change.
    """

    __tablename__ = "user_data_status"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("user.id", ondelete="CASCADE"), nullable=False)
    status = Column(SqlEnum(Status), nullable=False)
    modified_at = Column(
        DateTime, default=func.now(), onupdate=func.now(), nullable=False
    )
