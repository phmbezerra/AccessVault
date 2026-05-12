from fastapi import FastAPI
from app.database.connection import engine
from app.database.base import Base
from app.models.user import User
from app.models.system import System
from app.models.access import Access
from app.routes import users, auth, systems, accesses

app = FastAPI(title="AccessVault")

Base.metadata.create_all(bind=engine)

app.include_router(users.router, prefix="/users", tags=["Users"])
app.include_router(auth.router, prefix="/auth", tags=["Auth"])
app.include_router(systems.router, prefix="/systems", tags=["Systems"])
app.include_router(accesses.router, prefix="/accesses", tags=["Accesses"])


@app.get("/")
def read_root():
    return {"message": "AccessVault API online"}
