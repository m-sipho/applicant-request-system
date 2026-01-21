from pydantic import BaseModel, ConfigDict
from datetime import datetime
from enums import RequestType, StatusEnum
from typing import Dict, Any, Optional

class ShowRequest(BaseModel):
    id: int
    type: RequestType
    status: StatusEnum
    created_at: datetime

class CreateRequest(BaseModel):
    request_type: RequestType
    description: str
    metadata: Dict[str, Any]

class RequestOut(BaseModel):
    id: int
    type: str
    status: str
    description: str
    created_at: datetime
    updated_at: Optional[datetime] = None
    assignee_id: Optional[int] = None
    owner_id: int
    data: Dict[str, Any]

    model_config = ConfigDict(from_attributes=True)