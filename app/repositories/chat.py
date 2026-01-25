from typing import Optional, List
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, and_, desc
from app.models.user import ChatSession, Message, Recommendation
from app.repositories.base import BaseRepository
from app.schemas.user import ChatSessionCreate, ChatSessionUpdate, MessageCreate, MessageUpdate, RecommendationCreate


class ChatSessionRepository(BaseRepository[ChatSession]):
    async def create(self, db: AsyncSession, obj: ChatSessionCreate) -> ChatSession:
        db_obj = ChatSession(**obj.model_dump())
        db.add(db_obj)
        await db.commit()
        await db.refresh(db_obj)
        return db_obj

    async def get_by_id(self, db: AsyncSession, id: int) -> Optional[ChatSession]:
        result = await db.execute(select(ChatSession).where(ChatSession.id == id))
        return result.scalar_one_or_none()

    async def get_all(self, db: AsyncSession, skip: int = 0, limit: int = 100) -> List[ChatSession]:
        result = await db.execute(select(ChatSession).offset(skip).limit(limit))
        return result.scalars().all()

    async def get_user_sessions(self, db: AsyncSession, user_id: int, skip: int = 0, limit: int = 100) -> List[ChatSession]:
        result = await db.execute(
            select(ChatSession)
            .where(ChatSession.user_id == user_id)
            .order_by(desc(ChatSession.updated_at))
            .offset(skip).limit(limit)
        )
        return result.scalars().all()

    async def update(self, db: AsyncSession, id: int, obj: ChatSessionUpdate) -> Optional[ChatSession]:
        db_obj = await self.get_by_id(db, id)
        if db_obj:
            for key, value in obj.model_dump(exclude_unset=True).items():
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
        filters = [getattr(ChatSession, key) == value for key, value in kwargs.items()]
        stmt = select(ChatSession).where(and_(*filters)).limit(1)
        result = await db.execute(stmt)
        return result.scalar_one_or_none() is not None

    async def filter_by(self, db: AsyncSession, **kwargs) -> List[ChatSession]:
        filters = [getattr(ChatSession, key) == value for key, value in kwargs.items()]
        stmt = select(ChatSession).where(and_(*filters))
        result = await db.execute(stmt)
        return result.scalars().all()


class MessageRepository(BaseRepository[Message]):
    async def create(self, db: AsyncSession, obj: MessageCreate) -> Message:
        db_obj = Message(**obj.model_dump())
        db.add(db_obj)
        await db.commit()
        await db.refresh(db_obj)
        return db_obj

    async def get_by_id(self, db: AsyncSession, id: int) -> Optional[Message]:
        result = await db.execute(select(Message).where(Message.id == id))
        return result.scalar_one_or_none()

    async def get_messages_by_session(self, db: AsyncSession, session_id: int, skip: int = 0, limit: int = 100) -> List[Message]:
        result = await db.execute(
            select(Message)
            .where(Message.chat_session_id == session_id)
            .order_by(Message.timestamp.asc())
            .offset(skip).limit(limit)
        )
        return result.scalars().all()

    async def get_all(self, db: AsyncSession, skip: int = 0, limit: int = 100) -> List[Message]:
        result = await db.execute(select(Message).offset(skip).limit(limit))
        return result.scalars().all()

    async def update(self, db: AsyncSession, id: int, obj: MessageUpdate) -> Optional[Message]:
        db_obj = await self.get_by_id(db, id)
        if db_obj:
            for key, value in obj.model_dump(exclude_unset=True).items():
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
        filters = [getattr(Message, key) == value for key, value in kwargs.items()]
        stmt = select(Message).where(and_(*filters)).limit(1)
        result = await db.execute(stmt)
        return result.scalar_one_or_none() is not None

    async def filter_by(self, db: AsyncSession, **kwargs) -> List[Message]:
        filters = [getattr(Message, key) == value for key, value in kwargs.items()]
        stmt = select(Message).where(and_(*filters))
        result = await db.execute(stmt)
        return result.scalars().all()


class RecommendationRepository(BaseRepository[Recommendation]):
    async def create(self, db: AsyncSession, obj: RecommendationCreate) -> Recommendation:
        db_obj = Recommendation(**obj.model_dump())
        db.add(db_obj)
        await db.commit()
        await db.refresh(db_obj)
        return db_obj

    async def get_by_id(self, db: AsyncSession, id: int) -> Optional[Recommendation]:
        result = await db.execute(select(Recommendation).where(Recommendation.id == id))
        return result.scalar_one_or_none()

    async def get_recommendations_by_session(self, db: AsyncSession, session_id: int) -> List[Recommendation]:
        result = await db.execute(
            select(Recommendation)
            .where(Recommendation.chat_session_id == session_id)
        )
        return result.scalars().all()

    async def get_recommendations_by_car(self, db: AsyncSession, car_id: int) -> List[Recommendation]:
        result = await db.execute(
            select(Recommendation)
            .where(Recommendation.car_id == car_id)
        )
        return result.scalars().all()

    async def get_all(self, db: AsyncSession, skip: int = 0, limit: int = 100) -> List[Recommendation]:
        result = await db.execute(select(Recommendation).offset(skip).limit(limit))
        return result.scalars().all()

    async def update(self, db: AsyncSession, id: int, obj: dict) -> Optional[Recommendation]:
        db_obj = await self.get_by_id(db, id)
        if db_obj:
            for key, value in obj.items():
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
        filters = [getattr(Recommendation, key) == value for key, value in kwargs.items()]
        stmt = select(Recommendation).where(and_(*filters)).limit(1)
        result = await db.execute(stmt)
        return result.scalar_one_or_none() is not None

    async def filter_by(self, db: AsyncSession, **kwargs) -> List[Recommendation]:
        filters = [getattr(Recommendation, key) == value for key, value in kwargs.items()]
        stmt = select(Recommendation).where(and_(*filters))
        result = await db.execute(stmt)
        return result.scalars().all()