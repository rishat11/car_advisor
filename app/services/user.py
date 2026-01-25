import uuid
from typing import Optional, List, Tuple
from passlib.context import CryptContext
from datetime import datetime, timedelta
from jose import JWTError, jwt
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.config import settings
from app.repositories.user import UserRepository
from app.repositories.chat import ChatSessionRepository, MessageRepository, RecommendationRepository
from app.schemas.user import UserCreate, UserUpdate, UserInDB, CarCreate, CarUpdate, CarInDB, \
    ChatSessionCreate, ChatSessionUpdate, MessageCreate, MessageUpdate, RecommendationCreate, \
    ChatRequest, ChatResponse, CarPublic
from app.models.user import User, ChatSession, Message, Recommendation
from app.services.car import CarService


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto", bcrypt__rounds=12)


class UserService:
    def __init__(self):
        self.repository = UserRepository()

    def verify_password(self, plain_password: str, hashed_password: str) -> bool:
        return pwd_context.verify(plain_password, hashed_password)

    def get_password_hash(self, password: str) -> str:
        # Ensure password is not longer than 72 bytes for bcrypt
        if len(password.encode('utf-8')) > 72:
            password = password.encode('utf-8')[:72].decode('utf-8', errors='ignore')
        return pwd_context.hash(password)

    async def authenticate_user(self, db: AsyncSession, username: str, password: str) -> Optional[User]:
        user = await self.repository.get_by_username(db, username)
        if not user or not self.verify_password(password, user.hashed_password):
            return None
        return user

    async def authenticate_user_by_email(self, db: AsyncSession, email: str, password: str) -> Optional[User]:
        user = await self.repository.get_by_email(db, email)
        if not user or not self.verify_password(password, user.hashed_password):
            return None
        return user

    async def create_user(self, db: AsyncSession, user: UserCreate) -> UserInDB:
        # Check if password is too long for bcrypt (more than 72 bytes)
        if len(user.password.encode('utf-8')) > 72:
            raise ValueError("Password cannot be longer than 72 bytes")

        # Hash the password
        hashed_password = self.get_password_hash(user.password)

        # Create user object with hashed password
        # Pass the hashed password directly to the repository
        db_user = await self.repository.create_with_hashed_password(db, user, hashed_password)
        return UserInDB.from_orm(db_user)

    async def get_user_by_id(self, db: AsyncSession, user_id: int) -> Optional[UserInDB]:
        user = await self.repository.get_by_id(db, user_id)
        if user:
            return UserInDB.from_orm(user)
        return None

    async def get_user_by_username(self, db: AsyncSession, username: str) -> Optional[UserInDB]:
        user = await self.repository.get_by_username(db, username)
        if user:
            return UserInDB.from_orm(user)
        return None

    async def get_user_by_email(self, db: AsyncSession, email: str) -> Optional[UserInDB]:
        user = await self.repository.get_by_email(db, email)
        if user:
            return UserInDB.from_orm(user)
        return None

    async def update_user(self, db: AsyncSession, user_id: int, user_update: UserUpdate) -> Optional[UserInDB]:
        updated_user = await self.repository.update(db, user_id, user_update)
        if updated_user:
            return UserInDB.from_orm(updated_user)
        return None

    async def delete_user(self, db: AsyncSession, user_id: int) -> bool:
        return await self.repository.delete(db, user_id)




class ChatService:
    def __init__(self):
        self.session_repository = ChatSessionRepository()
        self.message_repository = MessageRepository()
        self.recommendation_repository = RecommendationRepository()
        self.car_service = CarService()

    async def create_session(self, db: AsyncSession, user_id: int, title: Optional[str] = None) -> ChatSession:
        session_data = ChatSessionCreate(user_id=user_id, title=title)
        return await self.session_repository.create(db, session_data)

    async def get_session_by_id(self, db: AsyncSession, session_id: int) -> Optional[ChatSession]:
        return await self.session_repository.get_by_id(db, session_id)

    async def get_user_sessions(self, db: AsyncSession, user_id: int, skip: int = 0, limit: int = 100) -> List[ChatSession]:
        return await self.session_repository.get_user_sessions(db, user_id, skip, limit)

    async def add_message(self, db: AsyncSession, session_id: int, user_id: Optional[int], 
                         content: str, role: str) -> Message:
        message_data = MessageCreate(
            chat_session_id=session_id,
            user_id=user_id,
            content=content,
            role=role
        )
        return await self.message_repository.create(db, message_data)

    async def get_session_messages(self, db: AsyncSession, session_id: int, skip: int = 0, limit: int = 100) -> List[Message]:
        return await self.message_repository.get_messages_by_session(db, session_id, skip, limit)

    async def add_recommendation(self, db: AsyncSession, session_id: int, car_id: int, reason: Optional[str] = None) -> Recommendation:
        recommendation_data = RecommendationCreate(
            chat_session_id=session_id,
            car_id=car_id,
            reason=reason
        )
        return await self.recommendation_repository.create(db, recommendation_data)

    async def get_session_recommendations(self, db: AsyncSession, session_id: int) -> List[Recommendation]:
        return await self.recommendation_repository.get_recommendations_by_session(db, session_id)

    async def process_chat_request(self, db: AsyncSession, user_id: int, chat_request: ChatRequest) -> ChatResponse:
        """
        Process a chat request and generate a response with car recommendations
        """
        # Get or create chat session
        if chat_request.session_id:
            session = await self.get_session_by_id(db, chat_request.session_id)
            if not session or session.user_id != user_id:
                raise ValueError("Invalid session ID")
        else:
            # Create new session
            session_title = f"Chat {datetime.now().strftime('%Y-%m-%d %H:%M')}"
            session = await self.create_session(db, user_id, title=session_title)

        # Add user message to session
        user_message = await self.add_message(
            db, session.id, user_id, chat_request.message, "user"
        )

        # Generate bot response based on user message
        # This is a simplified version - in a real app, you'd integrate with an LLM
        bot_response = await self.generate_bot_response(db, chat_request.message)

        # Add bot message to session
        bot_message = await self.add_message(
            db, session.id, None, bot_response.response, "assistant"
        )

        # Return the response
        return ChatResponse(
            response=bot_response.response,
            session_id=session.id,
            car_recommendations=bot_response.car_recommendations
        )

    async def generate_bot_response(self, db: AsyncSession, user_message: str) -> ChatResponse:
        """
        Generate a bot response based on the user's message using the recommendation engine.
        """
        # Import the recommendation engine here to avoid circular import
        from app.utils.car_recommender import recommendation_engine

        # Use the recommendation engine to process the query
        response_text, matching_cars = await recommendation_engine.process_query(db, user_message)

        return ChatResponse(
            response=response_text,
            session_id=0,  # Will be set by the calling function
            car_recommendations=matching_cars
        )


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    return encoded_jwt


def verify_token(token: str) -> Optional[dict]:
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            return None
        return payload
    except JWTError:
        return None