from typing import Optional, List
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, and_, func
from app.models.user import Car
from app.repositories.base import BaseRepository
from app.schemas.user import CarCreate, CarUpdate


class CarRepository(BaseRepository[Car]):
    async def create(self, db: AsyncSession, obj: CarCreate) -> Car:
        db_obj = Car(**obj.model_dump())
        db.add(db_obj)
        await db.commit()
        await db.refresh(db_obj)
        return db_obj

    async def get_by_id(self, db: AsyncSession, id: int) -> Optional[Car]:
        result = await db.execute(select(Car).where(Car.id == id))
        return result.scalar_one_or_none()

    async def get_all(self, db: AsyncSession, skip: int = 0, limit: int = 100) -> List[Car]:
        result = await db.execute(select(Car).offset(skip).limit(limit))
        return result.scalars().all()

    async def get_cars_by_filters(self, db: AsyncSession, 
                                  make: Optional[str] = None,
                                  min_year: Optional[int] = None,
                                  max_year: Optional[int] = None,
                                  body_type: Optional[str] = None,
                                  fuel_type: Optional[str] = None,
                                  min_price: Optional[float] = None,
                                  max_price: Optional[float] = None,
                                  skip: int = 0, 
                                  limit: int = 100) -> List[Car]:
        """Get cars filtered by various criteria"""
        stmt = select(Car)
        
        conditions = []
        if make:
            conditions.append(Car.make.ilike(f"%{make}%"))
        if min_year:
            conditions.append(Car.year >= min_year)
        if max_year:
            conditions.append(Car.year <= max_year)
        if body_type:
            conditions.append(Car.body_type == body_type)
        if fuel_type:
            conditions.append(Car.fuel_type == fuel_type)
        if min_price:
            conditions.append(Car.price >= min_price)
        if max_price:
            conditions.append(Car.price <= max_price)
            
        if conditions:
            stmt = stmt.where(and_(*conditions))
            
        stmt = stmt.offset(skip).limit(limit)
        result = await db.execute(stmt)
        return result.scalars().all()

    async def search_cars(self, db: AsyncSession, query: str, skip: int = 0, limit: int = 100) -> List[Car]:
        """Search cars by make, model, or features"""
        search_query = f"%{query}%"
        stmt = select(Car).where(
            and_(
                (Car.make.ilike(search_query)) |
                (Car.model.ilike(search_query)) |
                (Car.description.ilike(search_query)) |
                (Car.features.ilike(search_query))
            )
        ).offset(skip).limit(limit)
        
        result = await db.execute(stmt)
        return result.scalars().all()

    async def get_popular_cars(self, db: AsyncSession, limit: int = 10) -> List[Car]:
        """Get popular cars (this would typically be based on recommendation count or other metrics)"""
        # For now, just return most recently added cars
        stmt = select(Car).order_by(Car.created_at.desc()).limit(limit)
        result = await db.execute(stmt)
        return result.scalars().all()

    async def update(self, db: AsyncSession, id: int, obj: CarUpdate) -> Optional[Car]:
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
        filters = [getattr(Car, key) == value for key, value in kwargs.items()]
        stmt = select(Car).where(and_(*filters)).limit(1)
        result = await db.execute(stmt)
        return result.scalar_one_or_none() is not None

    async def filter_by(self, db: AsyncSession, **kwargs) -> List[Car]:
        filters = [getattr(Car, key) == value for key, value in kwargs.items()]
        stmt = select(Car).where(and_(*filters))
        result = await db.execute(stmt)
        return result.scalars().all()