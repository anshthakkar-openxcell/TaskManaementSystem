from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.models import SubTask

async def calculate_task_summary(db: AsyncSession, task_id: int):
    total = await db.execute(
        select(func.count()).where(SubTask.task_id == task_id)
    )

    completed = await db.execute(
        select(func.count()).where(
            SubTask.task_id == task_id,
            SubTask.is_completed == True
        )
    )

    total_count = total.scalar()
    completed_count = completed.scalar()

    return {
        "task_id": task_id,
        "total_subtasks": total_count,
        "completed_subtasks": completed_count,
        "pending_subtasks": total_count - completed_count
    }
