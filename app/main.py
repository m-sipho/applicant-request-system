from fastapi import FastAPI, HTTPException, status
from .schemas import CreateRequest
from .request_types import REQUEST_TYPE_RULES

app = FastAPI()


@app.get("/")
def root():
    return {"message": "Applicant Request System API. Go to /docs for API documentation."}