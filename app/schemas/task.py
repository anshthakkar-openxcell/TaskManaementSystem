from pydantic import BaseModel
from typing import Optional
from app.db.enums import TaskStatus
from app.schemas.pagination import PaginatedResponse


class TaskCreate(BaseModel):
    title: str
    description: Optional[str] = None
    status: TaskStatus = TaskStatus.PENDING


class TaskUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    status: Optional[TaskStatus] = None   


class TaskResponse(BaseModel):
    id: int
    title: str
    description: Optional[str] = None
    status: TaskStatus                     
    user_id: int

    model_config = {
        "from_attributes": True
    }


PaginatedTaskResponse = PaginatedResponse[TaskResponse]
