from fastapi import FastAPI
from app.db.database import engine, Base
from app.auth.routes import router as auth_router
from app.routes.task import router as task_router
from app.routes.substask import router as substask_router
from app.routes.task_summary import router as task_summary_router



app = FastAPI(
    title="Task Management API"

    )

@app.on_event("startup")
async def on_startup():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

app.include_router(auth_router)
app.include_router(task_router)
app.include_router(substask_router)
app.include_router(task_summary_router)