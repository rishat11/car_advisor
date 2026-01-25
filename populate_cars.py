import asyncio
import os
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from sqlalchemy import select
from app.models.user import Car
from app.core.config import settings
from app.db.session import engine
from faker import Faker
import random


fake = Faker('ru_RU')


async def create_sample_cars():
    """Populate the database with sample car data based on the cars.md specification"""

    async with AsyncSession(engine) as session:
        # Sample car data based on the specification in cars.md
        sample_cars = [
            # Toyota models
            {
                "make": "Toyota",
                "model": "Camry",
                "year": 2022,
                "body_type": "sedan",
                "fuel_type": "gasoline",
                "transmission": "automatic",
                "engine_size": 2.5,
                "horsepower": 203,
                "price": 2800000,
                "description": "Надежный седан бизнес-класса с отличной проходимостью и вместительным салоном.",
                "features": "Круиз-контроль, кожаный салон, камера заднего вида, Bluetooth"
            },
            {
                "make": "Toyota",
                "model": "RAV4",
                "year": 2023,
                "body_type": "crossover",
                "fuel_type": "hybrid",
                "transmission": "automatic",
                "engine_size": 2.5,
                "horsepower": 219,
                "price": 3200000,
                "description": "Популярный кроссовер с гибридной силовой установкой и высоким уровнем комфорта.",
                "features": "Полный привод, адаптивный круиз-контроль, камеры, беспроводная зарядка"
            },
            {
                "make": "Toyota",
                "model": "Land Cruiser Prado",
                "year": 2021,
                "body_type": "suv",
                "fuel_type": "gasoline",
                "transmission": "automatic",
                "engine_size": 4.0,
                "horsepower": 272,
                "price": 4500000,
                "description": "Внедорожник премиум-класса с отличной проходимостью и комфортным салоном.",
                "features": "Пневмоподвеска, центральный замок, климат-контроль, подогрев сидений"
            },

            # BMW models
            {
                "make": "BMW",
                "model": "X5",
                "year": 2023,
                "body_type": "suv",
                "fuel_type": "gasoline",
                "transmission": "automatic",
                "engine_size": 3.0,
                "horsepower": 340,
                "price": 6500000,
                "description": "Премиальный внедорожник с отличной динамикой и роскошным интерьером.",
                "features": "Система полного привода xDrive, адаптивная подвеска, панорамная крыша"
            },
            {
                "make": "BMW",
                "model": "3 Series",
                "year": 2022,
                "body_type": "sedan",
                "fuel_type": "gasoline",
                "transmission": "automatic",
                "engine_size": 2.0,
                "horsepower": 184,
                "price": 3000000,
                "description": "Спортивный седан с отличной управляемостью и современным интерьером.",
                "features": "Система iDrive, подогрев руля, датчики света и дождя, парктроник"
            },

            # Mercedes-Benz models
            {
                "make": "Mercedes-Benz",
                "model": "E-Class",
                "year": 2022,
                "body_type": "sedan",
                "fuel_type": "gasoline",
                "transmission": "automatic",
                "engine_size": 2.0,
                "horsepower": 258,
                "price": 5200000,
                "description": "Бизнес-седан премиум-класса с передовыми технологиями и комфортным салоном.",
                "features": "COMAND, подогрев сидений, ароматизатор воздуха, массаж сидений"
            },
            {
                "make": "Mercedes-Benz",
                "model": "GLC",
                "year": 2023,
                "body_type": "crossover",
                "fuel_type": "gasoline",
                "transmission": "automatic",
                "engine_size": 2.0,
                "horsepower": 258,
                "price": 4800000,
                "description": "Компактный кроссовер премиум-класса с отличной динамикой и вместительным салоном.",
                "features": "4MATIC, COMAND, панорамная крыша, адаптивный круиз-контроль"
            },

            # Honda models
            {
                "make": "Honda",
                "model": "CR-V",
                "year": 2022,
                "body_type": "crossover",
                "fuel_type": "gasoline",
                "transmission": "automatic",
                "engine_size": 1.5,
                "horsepower": 190,
                "price": 2600000,
                "description": "Надежный кроссовер с отличной вместимостью и экономичным двигателем.",
                "features": "Honda Sensing, Apple CarPlay, Android Auto, камера заднего вида"
            },
            {
                "make": "Honda",
                "model": "Accord",
                "year": 2021,
                "body_type": "sedan",
                "fuel_type": "gasoline",
                "transmission": "automatic",
                "engine_size": 1.5,
                "horsepower": 192,
                "price": 2400000,
                "description": "Комфортный седан с отличной шумоизоляцией и современным интерьером.",
                "features": "Honda Sensing, беспроводная зарядка, подогрев сидений, климат-контроль"
            },

            # Kia models
            {
                "make": "Kia",
                "model": "Sportage",
                "year": 2023,
                "body_type": "crossover",
                "fuel_type": "gasoline",
                "transmission": "automatic",
                "engine_size": 1.6,
                "horsepower": 200,
                "price": 2200000,
                "description": "Современный кроссовер с привлекательным дизайном и богатой комплектацией.",
                "features": "Панорамная крыша, беспроводная зарядка, подогрев руля, датчики света"
            },
            {
                "make": "Kia",
                "model": "Cerato",
                "year": 2022,
                "body_type": "sedan",
                "fuel_type": "gasoline",
                "transmission": "automatic",
                "engine_size": 1.6,
                "horsepower": 123,
                "price": 1800000,
                "description": "Компактный седан с отличным соотношением цены и качества.",
                "features": "Apple CarPlay, Android Auto, камера заднего вида, климат-контроль"
            },

            # Hyundai models
            {
                "make": "Hyundai",
                "model": "Tucson",
                "year": 2023,
                "body_type": "crossover",
                "fuel_type": "gasoline",
                "transmission": "automatic",
                "engine_size": 1.6,
                "horsepower": 180,
                "price": 2300000,
                "description": "Современный кроссовер с передовыми технологиями и стильным дизайном.",
                "features": "SmartSense, панорамная крыша, беспроводная зарядка, подогрев сидений"
            },
            {
                "make": "Hyundai",
                "model": "Solaris",
                "year": 2022,
                "body_type": "sedan",
                "fuel_type": "gasoline",
                "transmission": "manual",
                "engine_size": 1.4,
                "horsepower": 100,
                "price": 1200000,
                "description": "Экономичный седан с просторным салоном и надежным двигателем.",
                "features": "Bluetooth, USB, кондиционер, электростеклоподъемники"
            },

            # Marussia models (Russian supercar)
            {
                "make": "Marussia",
                "model": "B2",
                "year": 2018,
                "body_type": "coupe",
                "fuel_type": "gasoline",
                "transmission": "manual",
                "engine_size": 3.8,
                "horsepower": 300,
                "price": 8000000,
                "description": "Первый российский суперкар с кузовом из углепластика и спортивной подвеской.",
                "features": "Карбоновый обвес, спортивная подвеска, кожаный салон, аудиосистема"
            },

            # Koenigsegg models (Swedish hypercar)
            {
                "make": "Koenigsegg",
                "model": "CC850",
                "year": 2022,
                "body_type": "coupe",
                "fuel_type": "gasoline",
                "transmission": "manual",
                "engine_size": 5.0,
                "horsepower": 1060,
                "price": 40000000,
                "description": "Гиперкар с атмосферным двигателем V8 и ручной коробкой передач.",
                "features": "Carbon fiber body, racing seats, advanced aerodynamics, premium audio"
            }
        ]

        # Add sample cars to the database
        for car_data in sample_cars:
            # Check if car already exists
            existing_car = await session.execute(
                select(Car).where(
                    Car.make == car_data["make"],
                    Car.model == car_data["model"],
                    Car.year == car_data["year"]
                )
            )
            existing_car = existing_car.scalar_one_or_none()

            if not existing_car:
                car = Car(**car_data)
                session.add(car)

        await session.commit()
        print(f"Added {len(sample_cars)} sample cars to the database.")


if __name__ == "__main__":
    asyncio.run(create_sample_cars())