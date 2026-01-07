from sqlalchemy.ext.asyncio import AsyncSession
from app.db.models import User
from sqlalchemy.future import select

async def get_user_by_email(db: AsyncSession, email: str) -> User | None:
    """Fetch user from the database using email."""
    result = await db.execute(select(User).where(User.email == email))
    return result.scalars().first()
