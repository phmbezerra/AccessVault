from fastapi import FastAPI
from app.database.connection import engine
from app.database.base import Base
from app.models.user import User
from app.routes import users

app = FastAPI(title="AccessVault")

Base.metadata.create_all(bind=engine)

app.include_router(users.router, prefix="/users", tags=["Users"])


@app.get("/")
def read_root():
    return {"message": "AccessVault API online"}
