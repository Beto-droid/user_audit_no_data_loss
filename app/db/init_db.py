from app.db.session import Base, engine


def init_db():
    """Initialize the database(fast)"""
    Base.metadata.create_all(bind=engine)
