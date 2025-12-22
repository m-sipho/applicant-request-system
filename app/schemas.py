from pydantic import BaseModel
from typing import Dict, Any
from .request_types import RequestType

class CreateRequest(BaseModel):
    request_type: RequestType
    description: str
    metadata: Dict[str, Any]