from typing import Optional, List
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, and_
from app.models.user import User
from app.repositories.base import BaseRepository
from app.schemas.user import UserCreate, UserUpdate


class UserRepository(BaseRepository[User]):
    async def create(self, db: AsyncSession, obj: UserCreate) -> User:
        # This method expects the password to be already hashed
        db_obj = User(
            username=obj.username,
            email=obj.email,
            hashed_password=obj.password  # This should be hashed before passing here
        )
        db.add(db_obj)
        await db.commit()
        await db.refresh(db_obj)
        return db_obj

    async def create_with_hashed_password(self, db: AsyncSession, user_create: UserCreate, hashed_password: str) -> User:
        db_obj = User(
            username=user_create.username,
            email=user_create.email,
            hashed_password=hashed_password
        )
        db.add(db_obj)
        await db.commit()
        await db.refresh(db_obj)
        return db_obj

    async def get_by_id(self, db: AsyncSession, id: int) -> Optional[User]:
        result = await db.execute(select(User).where(User.id == id))
        return result.scalar_one_or_none()

    async def get_by_username(self, db: AsyncSession, username: str) -> Optional[User]:
        result = await db.execute(select(User).where(User.username == username))
        return result.scalar_one_or_none()

    async def get_by_email(self, db: AsyncSession, email: str) -> Optional[User]:
        result = await db.execute(select(User).where(User.email == email))
        return result.scalar_one_or_none()

    async def get_all(self, db: AsyncSession, skip: int = 0, limit: int = 100) -> List[User]:
        result = await db.execute(select(User).offset(skip).limit(limit))
        return result.scalars().all()

    async def update(self, db: AsyncSession, id: int, obj: UserUpdate) -> Optional[User]:
        db_obj = await self.get_by_id(db, id)
        if db_obj:
            for key, value in obj.dict(exclude_unset=True).items():
                setattr(db_obj, key, value)
            await db.commit()
            await db.refresh(db_obj)
        return db_obj

    async def delete(self, db: AsyncSession, id: int) -> bool:
        db_obj = await self.get_by_id(db, id)
        if db_obj:
            await db.delete(db_obj)
            await db.commit()
            return True
        return False

    async def exists(self, db: AsyncSession, **kwargs) -> bool:
        filters = [getattr(User, key) == value for key, value in kwargs.items()]
        stmt = select(User).where(and_(*filters)).limit(1)
        result = await db.execute(stmt)
        return result.scalar_one_or_none() is not None

    async def filter_by(self, db: AsyncSession, **kwargs) -> List[User]:
        filters = [getattr(User, key) == value for key, value in kwargs.items()]
        stmt = select(User).where(and_(*filters))
        result = await db.execute(stmt)
        return result.scalars().all()