from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select ,func
from typing import List, Optional
from fastapi import HTTPException

from app.schemas.task import TaskCreate, TaskUpdate, TaskResponse
from app.db.models import Task


async def create_task(
    db: AsyncSession,
    task: TaskCreate,
    user_id: int
) -> TaskResponse:
    new_task = Task(
        title=task.title,
        description=task.description,
        status=task.status,
        user_id=user_id
    )
    db.add(new_task)
    await db.commit()
    await db.refresh(new_task)

    return TaskResponse.model_validate(new_task)


async def get_tasks_by_user(
    db: AsyncSession,
    user_id: int,
    page: int,
    size: int,
) -> List[TaskResponse]:
    offset = (page - 1) * size
    total_result = await db.execute(
        select(func.count()).select_from(Task).where(Task.user_id == user_id)
    )
    total = total_result.scalar()
    result = await db.execute(
        select(Task)
        .where(Task.user_id == user_id)
        .offset(offset)
        .limit(size)
    )
    tasks = result.scalars().all()

    return {
        "items": [TaskResponse.model_validate(task) for task in tasks],
        "total": total,
        "page": page,
        "limit": size,
    }


async def get_task_by_id(
    db: AsyncSession,
    task_id: int
) -> TaskResponse:
    result = await db.execute(
        select(Task).where(Task.id == task_id)
    )
    task = result.scalars().first()

    if not task:
        raise HTTPException(status_code=404, detail="Task not found")

    return TaskResponse.model_validate(task)


async def update_task(
    db: AsyncSession,
    task_id: int,
    task_update: TaskUpdate
) -> TaskResponse:
    result = await db.execute(
        select(Task).where(Task.id == task_id)
    )
    task = result.scalars().first()

    if not task:
        raise HTTPException(status_code=404, detail="Task not found")

    if task_update.title is not None:
        task.title = task_update.title
    if task_update.description is not None:
        task.description = task_update.description
    if task_update.status is not None:
        task.status = task_update.status

    await db.commit()
    await db.refresh(task)

    return TaskResponse.model_validate(task)


async def delete_task(
    db: AsyncSession,
    task_id: int
) -> None:
    result = await db.execute(
        select(Task).where(Task.id == task_id)
    )
    task = result.scalars().first()

    if not task:
        raise HTTPException(status_code=404, detail="Task not found")

    await db.delete(task)
    await db.commit()

async def verify_task_owner(
    db: AsyncSession,
    task_id: int,
    user_id: int,
):
    result = await db.execute(
        select(Task).where(
            Task.id == task_id,
            Task.user_id == user_id
        )
    )
    task = result.scalars().first()

    if not task:
        raise HTTPException(
            status_code=404,
            detail="Task not found"
        )

    return task