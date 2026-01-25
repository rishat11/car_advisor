from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.session import get_db
from app.services.car import CarService
from app.core.security import get_current_user
from app.schemas.user import CarCreate, CarInDB, CarUpdate, CarPublic, SuccessResponse


router = APIRouter()
car_service = CarService()


@router.post("/", response_model=CarInDB, status_code=status.HTTP_201_CREATED)
async def create_car(
    car: CarCreate,
    current_user: dict = Depends(get_current_user),  # Admin check could be added here
    db: AsyncSession = Depends(get_db)
):
    # In a real app, you might check if the user has admin privileges
    db_car = await car_service.create_car(db, car)
    return db_car


@router.get("/", response_model=list[CarPublic])
async def get_cars(
    skip: int = 0,
    limit: int = 100,
    db: AsyncSession = Depends(get_db)
):
    cars = await car_service.get_all_cars(db, skip=skip, limit=limit)
    return [CarPublic.from_orm(car) for car in cars]


@router.get("/{car_id}", response_model=CarPublic)
async def get_car(car_id: int, db: AsyncSession = Depends(get_db)):
    car = await car_service.get_car_by_id(db, car_id)
    if not car:
        raise HTTPException(status_code=404, detail="Car not found")
    return CarPublic.from_orm(car)


@router.put("/{car_id}", response_model=CarInDB)
async def update_car(
    car_id: int,
    car_update: CarUpdate,
    current_user: dict = Depends(get_current_user),  # Admin check could be added here
    db: AsyncSession = Depends(get_db)
):
    updated_car = await car_service.update_car(db, car_id, car_update)
    if not updated_car:
        raise HTTPException(status_code=404, detail="Car not found")
    return updated_car


@router.delete("/{car_id}", response_model=SuccessResponse)
async def delete_car(
    car_id: int,
    current_user: dict = Depends(get_current_user),  # Admin check could be added here
    db: AsyncSession = Depends(get_db)
):
    deleted = await car_service.delete_car(db, car_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Car not found")
    return SuccessResponse(success=True, message="Car deleted successfully")


@router.get("/search/{query}", response_model=list[CarPublic])
async def search_cars(query: str, skip: int = 0, limit: int = 100, db: AsyncSession = Depends(get_db)):
    cars = await car_service.search_cars(db, query, skip=skip, limit=limit)
    return [CarPublic.from_orm(car) for car in cars]