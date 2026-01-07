from fastapi import FastAPI
from . import models
from .database import engine
from dotenv import load_dotenv
from .routers import root, authentication, bootstrap, requests, user, staff

load_dotenv()

app = FastAPI()

models.Base.metadata.create_all(bind=engine)

ENABLE_ADMIN_CREATION = True

app.include_router(root.router)

if ENABLE_ADMIN_CREATION:
    app.include_router(bootstrap.router)

app.include_router(authentication.router)
app.include_router(requests.router)
app.include_router(user.router)
app.include_router(staff.router)
