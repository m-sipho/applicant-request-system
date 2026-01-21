from fastapi import FastAPI
from app.core.database import Base, engine
from dotenv import load_dotenv
from fastapi.middleware.cors import CORSMiddleware
from app.modules.users.router import router as users_router, bootstrap
from app.modules.auth.router import router as auth_router
from app.modules.requests.router import router as requests_router


load_dotenv()

Base.metadata.create_all(bind=engine)

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "https://applicant-request-system.vercel.app"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

ENABLE_ADMIN_CREATION = True

@app.get("/")
async def root():
    return {"message": "Applicant Request System API. Go to /docs for API documentation."}

if ENABLE_ADMIN_CREATION:
    app.include_router(bootstrap)

app.include_router(auth_router)
app.include_router(requests_router)
app.include_router(users_router)
