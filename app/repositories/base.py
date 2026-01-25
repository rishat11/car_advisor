from abc import ABC, abstractmethod
from typing import Generic, TypeVar, List, Optional, Dict, Any
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.sql import Select


T = TypeVar('T')


class BaseRepository(ABC, Generic[T]):
    @abstractmethod
    async def create(self, db: AsyncSession, obj: T) -> T:
        pass

    @abstractmethod
    async def get_by_id(self, db: AsyncSession, id: int) -> Optional[T]:
        pass

    @abstractmethod
    async def get_all(self, db: AsyncSession, skip: int = 0, limit: int = 100) -> List[T]:
        pass

    @abstractmethod
    async def update(self, db: AsyncSession, id: int, obj: Dict[str, Any]) -> Optional[T]:
        pass

    @abstractmethod
    async def delete(self, db: AsyncSession, id: int) -> bool:
        pass

    @abstractmethod
    async def exists(self, db: AsyncSession, **kwargs) -> bool:
        pass

    @abstractmethod
    async def filter_by(self, db: AsyncSession, **kwargs) -> List[T]:
        pass