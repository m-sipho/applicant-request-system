from fastapi import APIRouter

router = APIRouter(
    tags=["Root"]
)

@router.get("/")
async def root():
    return {"message": "Applicant Request System API. Go to /docs for API documentation."}