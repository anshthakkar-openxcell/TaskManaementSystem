from sqlalchemy.ext.asyncio import AsyncSession
from app.schemas.subtask import SubtaskCreate, SubtaskUpdate, SubtaskResponse
from app.db.models import SubTask  
from app.db.database import get_db
from sqlalchemy import select, update, delete


async def create_subtask(db: AsyncSession, subtask: SubtaskCreate) -> SubtaskResponse:
    new_subtask = SubTask(
        title=subtask.title,
        description=subtask.description,
        is_completed=subtask.is_completed,
        task_id=subtask.task_id
    )
    db.add(new_subtask)
    await db.commit()
    await db.refresh(new_subtask)
    return subtaskResponse.from_orm(new_subtask)


async def get_subtasks_by_task(db: AsyncSession, task_id: int) -> list[SubtaskResponse]:
    result = await db.execute(select(SubTask).where(SubTask.task_id == task_id))
    subtasks = result.scalars().all()
    return [SubtaskResponse.from_orm(subtask) for subtask in subtasks]

async def update_subtask(db: AsyncSession, subtask_id: int, subtask_update: SubtaskUpdate) -> SubtaskResponse:
    result = await db.execute(select(SubTask).where(SubTask.id == subtask_id))
    subtask = result.scalars().first()
    if not subtask:
        raise ValueError("Subtask not found.")

    if subtask_update.title is not None:
        subtask.title = subtask_update.title
    if subtask_update.description is not None:
        subtask.description = subtask_update.description
    if subtask_update.is_completed is not None:
        subtask.is_completed = subtask_update.is_completed

    db.add(subtask)
    await db.commit()
    await db.refresh(subtask)
    return SubtaskResponse.from_orm(subtask)

async def delete_subtask(db: AsyncSession, subtask_id: int) -> None:
    result = await db.execute(select(SubTask).where(SubTask.id == subtask_id))
    subtask = result.scalars().first()
    if not subtask:
        raise ValueError("Subtask not found.")

    await db.delete(subtask)
    await db.commit()

async def get_subtask_by_id(db: AsyncSession, subtask_id: int) -> SubtaskResponse:
    result = await db.execute(select(SubTask).where(SubTask.id == subtask_id))
    subtask = result.scalars().first()
    if subtask:
        return SubtaskResponse.from_orm(subtask)
    return None

