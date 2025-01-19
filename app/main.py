from fastapi import FastAPI
from app.api.controllers import users
from app.db.init_db import init_db

app = FastAPI()

app.include_router(users.router)

# Disable for to use alembic
init_db()


@app.get("/")
def read_root():
    return {"message": "Welcome to FastAPI"}
