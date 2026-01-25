from datetime import datetime
from typing import Optional
from sqlalchemy import String, Text, DateTime, Integer, ForeignKey, Boolean, UniqueConstraint, Float
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.models.base import Base


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    username: Mapped[str] = mapped_column(String(50), unique=True, index=True, nullable=False)
    email: Mapped[str] = mapped_column(String(100), unique=True, index=True, nullable=False)
    hashed_password: Mapped[str] = mapped_column(String(255), nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    is_verified: Mapped[bool] = mapped_column(Boolean, default=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    chat_sessions: Mapped[list["ChatSession"]] = relationship("ChatSession", back_populates="user", cascade="all, delete-orphan")
    messages: Mapped[list["Message"]] = relationship("Message", back_populates="user", cascade="all, delete-orphan")


class Car(Base):
    __tablename__ = "cars"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    make: Mapped[str] = mapped_column(String(50), nullable=False)
    model: Mapped[str] = mapped_column(String(100), nullable=False)
    year: Mapped[int] = mapped_column(Integer, nullable=False)
    body_type: Mapped[str] = mapped_column(String(50), nullable=False)  # sedan, suv, hatchback, etc.
    fuel_type: Mapped[str] = mapped_column(String(50), nullable=False)  # gasoline, diesel, electric, hybrid
    transmission: Mapped[str] = mapped_column(String(20), nullable=False)  # manual, automatic
    engine_size: Mapped[Optional[float]] = mapped_column(Float)  # in liters
    horsepower: Mapped[Optional[int]] = mapped_column(Integer)  # in HP
    price: Mapped[Optional[float]] = mapped_column(Float)  # in USD
    description: Mapped[Optional[str]] = mapped_column(Text)
    features: Mapped[Optional[str]] = mapped_column(Text)  # comma-separated features
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    recommendations: Mapped[list["Recommendation"]] = relationship("Recommendation", back_populates="car", cascade="all, delete-orphan")
    features_obj: Mapped[list["CarFeature"]] = relationship("CarFeature", secondary="car_feature_associations", back_populates="cars")


class ChatSession(Base):
    __tablename__ = "chat_sessions"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey("users.id"), nullable=False)
    title: Mapped[str] = mapped_column(String(200), nullable=True)  # auto-generated title from first message
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    user: Mapped["User"] = relationship("User", back_populates="chat_sessions")
    messages: Mapped[list["Message"]] = relationship("Message", back_populates="chat_session", cascade="all, delete-orphan")
    recommendations: Mapped[list["Recommendation"]] = relationship("Recommendation", back_populates="chat_session", cascade="all, delete-orphan")


class Message(Base):
    __tablename__ = "messages"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    chat_session_id: Mapped[int] = mapped_column(Integer, ForeignKey("chat_sessions.id"), nullable=False)
    user_id: Mapped[Optional[int]] = mapped_column(Integer, ForeignKey("users.id"))  # null for bot messages
    content: Mapped[str] = mapped_column(Text, nullable=False)
    role: Mapped[str] = mapped_column(String(20), nullable=False)  # 'user' or 'assistant'
    timestamp: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    # Relationships
    chat_session: Mapped["ChatSession"] = relationship("ChatSession", back_populates="messages")
    user: Mapped[Optional["User"]] = relationship("User", back_populates="messages")


class Recommendation(Base):
    __tablename__ = "recommendations"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    chat_session_id: Mapped[int] = mapped_column(Integer, ForeignKey("chat_sessions.id"), nullable=False)
    car_id: Mapped[int] = mapped_column(Integer, ForeignKey("cars.id"), nullable=False)
    reason: Mapped[Optional[str]] = mapped_column(Text)  # why this car was recommended
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    # Relationships
    chat_session: Mapped["ChatSession"] = relationship("ChatSession", back_populates="recommendations")
    car: Mapped["Car"] = relationship("Car", back_populates="recommendations")

    # Constraints
    __table_args__ = (UniqueConstraint('chat_session_id', 'car_id', name='unique_chat_car_recommendation'),)


class CarFeature(Base):
    __tablename__ = "car_features"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String(100), unique=True, nullable=False)  # ABS, Airbags, etc.
    description: Mapped[Optional[str]] = mapped_column(Text)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    # Relationships
    cars: Mapped[list["Car"]] = relationship("Car", secondary="car_feature_associations", back_populates="features_obj")


class CarFeatureAssociation(Base):
    __tablename__ = "car_feature_associations"

    car_id: Mapped[int] = mapped_column(Integer, ForeignKey("cars.id"), primary_key=True)
    feature_id: Mapped[int] = mapped_column(Integer, ForeignKey("car_features.id"), primary_key=True)