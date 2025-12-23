from fastapi import FastAPI, HTTPException, status, Depends
from .schemas import CreateRequest, CreateUser, RoleEnum
from .request_types import REQUEST_TYPE_RULES
from . import models, database
from .database import engine
from sqlalchemy.orm import Session
from .hashing import Hash

app = FastAPI()

models.Base.metadata.create_all(bind=engine)

@app.get("/")
def root():
    return {"message": "Applicant Request System API. Go to /docs for API documentation."}

@app.post("/request", status_code=status.HTTP_201_CREATED)
def create_request(request: CreateRequest, db: Session = Depends(database.get_db)):
    rules = REQUEST_TYPE_RULES.get(request.request_type)

    if not rules:
        raise HTTPException (
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Unsupported request type"
        )
    required_fields = rules["required"]
    
    for field_name, field_type in required_fields.items():
        if field_name not in request.metadata:
             raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Missing required field: {field_name}"
            )
        if not isinstance(request.metadata[field_name], field_type):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Invalid type of field: {field_name}"
            )
    
    new_request = models.Request(type=request.request_type, description=request.description, data=request.metadata)
    db.add(new_request)
    db.commit()
    db.refresh(new_request)

    return new_request

@app.post("/user", status_code=status.HTTP_201_CREATED)
def create_user(request: CreateUser, db: Session = Depends(database.get_db)):
    # Check for existing user
    existing = db.query(models.User).filter(models.User.email == request.email).first()
    if existing:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Email already registered"
        )
    new_user = models.User(
        name=request.name,
        email=request.email,
        password=Hash.get_password_hashed(request.password),
        role=RoleEnum.student
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user