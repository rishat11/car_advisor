import uuid
from typing import Optional, List
from sqlalchemy.ext.asyncio import AsyncSession
from app.repositories.car import CarRepository
from app.schemas.user import CarCreate, CarUpdate, CarInDB, CarPublic


class CarService:
    def __init__(self):
        self.repository = CarRepository()

    async def create_car(self, db: AsyncSession, car: CarCreate) -> CarInDB:
        db_car = await self.repository.create(db, car)
        return CarInDB.from_orm(db_car)

    async def get_car_by_id(self, db: AsyncSession, car_id: int) -> Optional[CarInDB]:
        car = await self.repository.get_by_id(db, car_id)
        if car:
            return CarInDB.from_orm(car)
        return None

    async def get_all_cars(self, db: AsyncSession, skip: int = 0, limit: int = 100) -> List[CarInDB]:
        cars = await self.repository.get_all(db, skip, limit)
        return [CarInDB.from_orm(car) for car in cars]

    async def get_cars_by_filters(self, db: AsyncSession,
                                  make: Optional[str] = None,
                                  min_year: Optional[int] = None,
                                  max_year: Optional[int] = None,
                                  body_type: Optional[str] = None,
                                  fuel_type: Optional[str] = None,
                                  min_price: Optional[float] = None,
                                  max_price: Optional[float] = None,
                                  transmission: Optional[str] = None,  # Added transmission parameter
                                  min_horsepower: Optional[int] = None,  # Added horsepower parameter
                                  skip: int = 0,
                                  limit: int = 100) -> List[CarInDB]:
        cars = await self.repository.get_cars_by_filters(
            db, make, min_year, max_year, body_type, fuel_type,
            min_price, max_price, skip, limit
        )
        # Additional filtering for transmission and horsepower if needed
        filtered_cars = []
        for car in cars:
            # Apply transmission filter
            if transmission and car.transmission != transmission:
                continue

            # Apply horsepower filter
            if min_horsepower and (not car.horsepower or car.horsepower < min_horsepower):
                continue

            filtered_cars.append(car)

        return filtered_cars[:limit]

    async def search_cars(self, db: AsyncSession, query: str, skip: int = 0, limit: int = 100) -> List[CarInDB]:
        cars = await self.repository.search_cars(db, query, skip, limit)
        return [CarInDB.from_orm(car) for car in cars]

    async def get_popular_cars(self, db: AsyncSession, limit: int = 10) -> List[CarInDB]:
        cars = await self.repository.get_popular_cars(db, limit)
        return [CarInDB.from_orm(car) for car in cars]

    async def update_car(self, db: AsyncSession, car_id: int, car_update: CarUpdate) -> Optional[CarInDB]:
        updated_car = await self.repository.update(db, car_id, car_update)
        if updated_car:
            return CarInDB.from_orm(updated_car)
        return None

    async def delete_car(self, db: AsyncSession, car_id: int) -> bool:
        return await self.repository.delete(db, car_id)