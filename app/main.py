from fastapi import FastAPI, HTTPException, status
from .schemas import CreateRequest
from .request_types import REQUEST_TYPE_RULES

app = FastAPI()


@app.get("/")
def root():
    return {"message": "Applicant Request System API. Go to /docs for API documentation."}

@app.post("/request", status_code=status.HTTP_201_CREATED)
def create_request(request: CreateRequest):
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
    
    return request.metadata