from pydantic import BaseModel
from typing import Optional
from app.schemas.pagination import PaginatedResponse

class SubtaskCreate(BaseModel):
    title: str
    description: Optional[str] = None
    task_id: int
    is_completed: Optional[bool] = False

class SubtaskUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    is_completed: Optional[bool] = None

class SubtaskResponse(BaseModel):
    id: int
    title: str
    description: Optional[str] = None
    task_id: int
    is_completed: bool

    model_config = {
        "from_attributes": True
    }

PaginatedSubtaskResponse = PaginatedResponse[SubtaskResponse]