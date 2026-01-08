from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.database import get_db
from app.services.task_service import create_task, get_tasks_by_user, get_task_by_id, update_task, delete_task, verify_task_owner
from app.schemas.task import TaskCreate, TaskUpdate, TaskResponse
from app.schemas.task import PaginatedTaskResponse
from typing import List
from app.auth.utils import get_current_user_id
from app.schemas.subtask import SubtaskCreate, SubtaskResponse
from app.services.subtask_service import create_subtask_service ,get_subtask_by_id ,get_subtasks_by_task

router = APIRouter(prefix="/tasks", tags=["tasks"])

@router.post("", response_model=TaskResponse)
async def create_new_task(
    task: TaskCreate,
    db: AsyncSession = Depends(get_db),
    user_id: int = Depends(get_current_user_id)
):
    task_response = await create_task(db, task, user_id)
    return task_response

@router.get("/", response_model=PaginatedTaskResponse)
async def read_my_tasks(
    page: int = Query(1, ge=1),
    size: int = Query(10, ge=1, le=100),
    db: AsyncSession = Depends(get_db),
    user_id: int = Depends(get_current_user_id),
):
    tasks = await get_tasks_by_user(db, user_id, page, size)
    return tasks

@router.get("/{task_id}", response_model=TaskResponse)
async def read_task(
    task_id: int,
    db: AsyncSession = Depends(get_db),
    user_id: int = Depends(get_current_user_id)
):
    task = await get_task_by_id(db, task_id)
    if task.user_id != user_id:
        raise HTTPException(status_code=403, detail="Not authorized to access this task")
    return task

@router.put("/{task_id}", response_model=TaskResponse)
async def update_existing_task(
    task_id: int,
    task_update: TaskUpdate,
    db: AsyncSession = Depends(get_db),
    user_id: int = Depends(get_current_user_id)
):
    task = await get_task_by_id(db, task_id)
    if task.user_id != user_id:
        raise HTTPException(status_code=403, detail="Not authorized to update this task")
    updated_task = await update_task(db, task_id, task_update)
    return updated_task

@router.delete("/{task_id}", response_model=dict)
async def delete_existing_task(
    task_id: int,
    db: AsyncSession = Depends(get_db),
    user_id: int = Depends(get_current_user_id)
):
    task = await get_task_by_id(db, task_id)
    if task.user_id != user_id:
        raise HTTPException(status_verify_task_ownercode=403, detail="Not authorized to delete this task")
    await delete_task(db, task_id)
    return {"message": "Task deleted successfully."}

@router.post("/{task_id}/subtasks", response_model=SubtaskResponse)
async def create_subtask(
    task_id: int,
    subtask: SubtaskCreate,
    db: AsyncSession = Depends(get_db),
    user_id: int = Depends(get_current_user_id)
):
    await verify_task_owner(db, task_id, user_id)
    subtask.task_id = task_id   
    subtask_response = await create_subtask_service(db, subtask)
    return subtask_response

@router.get("/{task_id}/subtasks", response_model=List[SubtaskResponse])
async def read_subtasks_for_task(
    task_id: int,
    db: AsyncSession = Depends(get_db),
    user_id: int = Depends(get_current_user_id)
):
    await verify_task_owner(db, task_id, user_id)
    subtasks = await get_subtasks_by_task(db, task_id)
    return subtasks

@router.get("/{task_id}/subtasks/{subtask_id}", response_model=SubtaskResponse)
async def read_subtask(
    task_id: int,
    subtask_id: int,
    db: AsyncSession = Depends(get_db),
    user_id: int = Depends(get_current_user_id)
):
    await verify_task_owner(db, task_id, user_id)
    subtask = await get_subtask_by_id(db, subtask_id)
    if not subtask or subtask.task_id != task_id:
        raise HTTPException(status_code=404, detail="Subtask not found")
    return subtask