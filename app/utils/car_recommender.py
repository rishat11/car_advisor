import re
from typing import Dict, List, Optional, Tuple
from app.services.car import CarService
from app.schemas.user import CarPublic


class CarRecommendationEngine:
    """
    Advanced car recommendation engine that processes natural language queries
    and matches them to cars in the database based on extracted parameters.
    """
    
    def __init__(self):
        self.car_service = CarService()
        self.parameter_keywords = {
            'body_type': {
                'sedan': ['седан', 'седане', 'купе', 'купе'],
                'suv': ['внедорожник', 'внедорожнике', 'джип', 'паркетник', 'кроссовер', 'кроссовере'],
                'hatchback': ['хэтчбек', 'хетчбек', 'универсал', 'минивен'],
                'truck': ['пикап', 'грузовик', 'трак']
            },
            'fuel_type': {
                'gasoline': ['бензин', 'бензиновый', 'октан'],
                'diesel': ['дизель', 'дизельный', 'турбодизель'],
                'hybrid': ['гибрид', 'гибридный', 'электрогибрид'],
                'electric': ['электро', 'электромобиль', 'электрокар', 'ev', 'electric']
            },
            'transmission': {
                'automatic': ['автомат', 'автоматическая', 'автоматик', 'ат'],
                'manual': ['механика', 'механическая', 'ручная', 'мт'],
                'cvt': ['вариатор', 'cvt', 'вариаторная']
            },
            'make': {
                'Toyota': ['тойота', 'toyota', 'камри', 'рав4', 'ленд крузер'],
                'BMW': ['бмв', 'bmw', 'бавария'],
                'Mercedes': ['мерседес', 'мерс', 'benz', 'клс', 'е класс'],
                'Honda': ['хонда', 'honda', 'сivic', 'cr-v'],
                'Kia': ['киа', 'kia', 'спортейдж', 'керато'],
                'Hyundai': ['хендай', 'hyundai', 'туссан', 'соната'],
                'Marussia': ['маруся', 'marussia', 'б2'],
                'Koenigsegg': ['кенигсегг', 'koenigsegg', 'cc850']
            }
        }
        
        # Price-related keywords
        self.price_keywords = [
            'бюджет', 'цена', 'стоимость', 'дорогой', 'дешевый', 'недорогой', 
            'дешевле', 'дороже', 'до', 'менее', 'более', 'около', 'примерно'
        ]
        
        # Year-related keywords
        self.year_keywords = [
            'год', 'выпуск', 'новый', 'старый', 'новее', 'старше', 'свежий'
        ]

    def extract_parameters(self, query: str) -> Dict[str, any]:
        """
        Extract car parameters from a natural language query
        """
        query_lower = query.lower()
        params = {}
        
        # Extract body type
        for body_type, keywords in self.parameter_keywords['body_type'].items():
            if any(keyword in query_lower for keyword in keywords):
                params['body_type'] = body_type
        
        # Extract fuel type
        for fuel_type, keywords in self.parameter_keywords['fuel_type'].items():
            if any(keyword in query_lower for keyword in keywords):
                params['fuel_type'] = fuel_type
        
        # Extract transmission
        for transmission, keywords in self.parameter_keywords['transmission'].items():
            if any(keyword in query_lower for keyword in keywords):
                params['transmission'] = transmission
        
        # Extract make
        for make, keywords in self.parameter_keywords['make'].items():
            if any(keyword in query_lower for keyword in keywords):
                params['make'] = make
        
        # Extract price range
        price_match = re.search(r'(\d{1,3}(?:\s*\d{3})*)\s*(?:руб|рублей|тыс|тысяч|млн|миллион)', query_lower)
        if price_match:
            price_str = price_match.group(1).replace(' ', '')
            price = int(price_str)
            
            # Adjust for units
            if 'тыс' in query_lower or 'тысяч' in query_lower:
                price *= 1000
            elif 'млн' in query_lower or 'миллион' in query_lower:
                price *= 1000000
            
            # Determine if it's max price or min price based on context
            if any(word in query_lower for word in ['до', 'менее', 'не_больше', 'бюджет']):
                params['max_price'] = price
            elif any(word in query_lower for word in ['более', 'больше', 'от']):
                params['min_price'] = price
            else:
                # Default to max price if not specified
                params['max_price'] = price
        
        # Extract year range
        year_match = re.search(r'(?:\b(20\d{2})\b)', query_lower)
        if year_match:
            year = int(year_match.group(1))
            if any(word in query_lower for word in ['новый', 'новее', 'свежий']):
                params['min_year'] = year
            elif any(word in query_lower for word in ['старый', 'старше']):
                params['max_year'] = year
            else:
                params['year'] = year
        
        # Extract power (horsepower)
        hp_match = re.search(r'(\d+)\s*(?:л\.с\.|лс|лошадиных)', query_lower)
        if hp_match:
            power = int(hp_match.group(1))
            if any(word in query_lower for word in ['мощнее', 'мощный', 'мощность']):
                params['min_horsepower'] = power
            else:
                params['horsepower'] = power
        
        return params

    async def find_matching_cars(self, db, params: Dict[str, any], limit: int = 5) -> List[CarPublic]:
        """
        Find cars that match the extracted parameters
        """
        # Map our parameters to the car service parameters
        filters = {}
        
        if 'make' in params:
            filters['make'] = params['make']
        if 'body_type' in params:
            filters['body_type'] = params['body_type']
        if 'fuel_type' in params:
            filters['fuel_type'] = params['fuel_type']
        if 'transmission' in params:
            filters['transmission'] = params['transmission']
        if 'min_year' in params:
            filters['min_year'] = params['min_year']
        if 'max_year' in params:
            filters['max_year'] = params['max_year']
        if 'year' in params:
            filters['min_year'] = params['year']
            filters['max_year'] = params['year'] + 1
        if 'min_price' in params:
            filters['min_price'] = params['min_price']
        if 'max_price' in params:
            filters['max_price'] = params['max_price']
        if 'min_horsepower' in params:
            # Note: Our car service doesn't have min_horsepower filter, so we'll need to filter after
            pass
        
        # Get cars from the database
        cars = await self.car_service.get_cars_by_filters(db, **filters, limit=limit*2)  # Get more to account for additional filtering
        
        # Additional filtering for horsepower if needed
        if 'min_horsepower' in params:
            min_hp = params['min_horsepower']
            cars = [car for car in cars if car.horsepower and car.horsepower >= min_hp]
        
        # Limit to desired number
        return cars[:limit]

    def generate_response(self, query: str, matching_cars: List[CarPublic]) -> str:
        """
        Generate a natural language response based on the query and matching cars
        """
        if not matching_cars:
            return (
                "К сожалению, я не нашел автомобилей, соответствующих вашему запросу. "
                "Попробуйте изменить параметры поиска или уточнить ваш запрос."
            )
        
        response = f"Я нашел {len(matching_cars)} автомобиль(ей), которые могут вам подойти:\n\n"
        
        for i, car in enumerate(matching_cars, 1):
            response += (
                f"{i}. **{car.make} {car.model}** ({car.year} г.)\n"
                f"   - Тип кузова: {car.body_type}\n"
                f"   - Тип топлива: {car.fuel_type}\n"
                f"   - Коробка передач: {car.transmission}\n"
            )
            
            if car.engine_size:
                response += f"   - Объем двигателя: {car.engine_size} л.\n"
            if car.horsepower:
                response += f"   - Мощность: {car.horsepower} л.с.\n"
            if car.price:
                response += f"   - Цена: {car.price:,.0f} руб.\n"
            
            if car.description:
                response += f"   - Описание: {car.description[:100]}...\n"
            
            response += "\n"
        
        if len(matching_cars) == 1:
            response += "Это единственный автомобиль, соответствующий вашему запросу. "
        else:
            response += f"Выберите понравившийся вариант, и я могу рассказать о нем подробнее."
        
        return response

    async def process_query(self, db, query: str) -> Tuple[str, List[CarPublic]]:
        """
        Main method to process a user query and return a response with car recommendations
        """
        # Extract parameters from the query
        params = self.extract_parameters(query)
        
        # Find matching cars
        matching_cars = await self.find_matching_cars(db, params)
        
        # Generate response
        response = self.generate_response(query, matching_cars)
        
        return response, matching_cars


# Global instance of the recommendation engine
recommendation_engine = CarRecommendationEngine()