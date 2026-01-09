from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.database import get_db
from app.services.task_summary_service import calculate_task_summary
from app.auth.utils import get_current_user_id
from app.core.redis import redis_client
import json
router = APIRouter(prefix="/task_summary", tags=["task_summary"])

@router.get("/{task_id}", response_model=dict)
async def get_task_summary(
    task_id: int,
    db: AsyncSession = Depends(get_db),
    user_id: int = Depends(get_current_user_id)
):
    cache_key = f"task_summary:{task_id}"
    cached_summary = await redis_client.get(cache_key)
    if cached_summary:
        return json.loads(cached_summary)
    summary = await calculate_task_summary(db, task_id)
    await redis_client.set(cache_key, json.dumps(summary), ex=20)  
    return summary