from fastapi import FastAPI
from . import models
from .database import engine
from dotenv import load_dotenv
from .routers import register, root, authentication, bootstrap, requests, staff
from fastapi.middleware.cors import CORSMiddleware

load_dotenv()

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

ENABLE_ADMIN_CREATION = True

app.include_router(root.router)

if ENABLE_ADMIN_CREATION:
    app.include_router(bootstrap.router)

app.include_router(authentication.router)
app.include_router(requests.router)
app.include_router(register.router)
app.include_router(staff.router)
