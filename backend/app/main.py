from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.database.connection import engine
from app.database.base import Base
from app.models.user import User
from app.models.system import System
from app.models.access import Access
from app.models.request import AccessRequest
from app.routes import users, auth, systems, accesses, dashboard
from app.routes import requests

app = FastAPI(title="AccessVault")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

Base.metadata.create_all(bind=engine)

app.include_router(users.router, prefix="/users", tags=["Users"])
app.include_router(auth.router, prefix="/auth", tags=["Auth"])
app.include_router(systems.router, prefix="/systems", tags=["Systems"])
app.include_router(accesses.router, prefix="/accesses", tags=["Accesses"])
app.include_router(dashboard.router, prefix="/dashboard", tags=["Dashboard"])
app.include_router(requests.router, prefix="/requests", tags=["Requests"])


@app.get("/")
def read_root():
    return {"message": "AccessVault API online"}