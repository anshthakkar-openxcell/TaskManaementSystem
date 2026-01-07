from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import APIRouter, Depends, HTTPException, Query
from app.db.database import get_db
from app.services.subtask_service import update_subtask, delete_subtask
from app.schemas.subtask import SubtaskUpdate, SubtaskResponse
from typing import List
from app.auth.utils import get_current_user_id
from app.services.task_service import verify_task_owner


router = APIRouter(prefix="/subtasks", tags=["subtasks"])

@router.put("/{substask_id}", response_model=SubtaskResponse)
async def update_existing_substask(
    substask_id: int,
    substask_update: SubtaskUpdate,
    db: AsyncSession = Depends(get_db),
    user_id: int = Depends(get_current_user_id)
):
    await verify_task_owner(db, task_id, user_id)
    updated_substask = await update_subtask(db, substask_id, substask_update)
    return updated_substask


@router.delete("/{substask_id}", response_model=dict)
async def delete_existing_substask(
    substask_id: int,
    db: AsyncSession = Depends(get_db),
    user_id: int = Depends(get_current_user_id)
):
    await verify_task_owner(db, task_id, user_id)
    await delete_subtask(db, substask_id)
    return {"detail": "Subtask deleted successfully"}