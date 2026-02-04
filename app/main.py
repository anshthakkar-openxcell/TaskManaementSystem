from fastapi import FastAPI
from app.db.database import engine, Base
from app.auth.routes import router as auth_router
from app.routes.task import router as task_router
from app.routes.substask import router as substask_router
from app.routes.task_summary import router as task_summary_router
import os
from alembic.config import Config
from alembic import command



app = FastAPI(
    title="Task Management API"

    )

@app.on_event("startup")
async def on_startup():
    # Check if database file exists
    db_path = "./taskmanagement.db"
    if not os.path.exists(db_path):
        # Run Alembic upgrade to create tables
        alembic_cfg = Config("alembic.ini")
        command.upgrade(alembic_cfg, "head")
    # If exists, assume tables are already created via migrations

app.include_router(auth_router)
app.include_router(task_router)
app.include_router(substask_router)
app.include_router(task_summary_router)