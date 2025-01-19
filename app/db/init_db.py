from app.db.session import Base, engine
import app.models


def init_db():
    """Initialize the database(fast)"""
    Base.metadata.create_all(bind=engine)
