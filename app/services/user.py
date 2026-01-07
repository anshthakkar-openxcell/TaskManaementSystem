from app.auth.schema import UserResponse  # Import UserResponse
from app.db.models import User
from app.auth.utils import hash_password
from sqlalchemy.ext.asyncio import AsyncSession
from app.auth.schema import UserCreate


async def create_user(db: AsyncSession, user: UserCreate):
    # Create the user record
    user_db = User(
        name=user.name,
        email=user.email,
        hashed_password=hash_password(user.password)
    )

    db.add(user_db)
    await db.commit()
    await db.refresh(user_db)

    # Return the UserResponse object, matching the expected fields
    return UserResponse(
        id=user_db.id,       
        name=user_db.name,  
        email=user_db.email   
    )
