# Car Advisor - AI-Powered Car Recommendation System

Car Advisor is a production-ready FastAPI backend for a car recommendation chat service. The system allows users to interact with an AI assistant to find suitable cars based on their needs and preferences.

## Features

- **JWT Authentication**: Secure user authentication with access and refresh tokens
- **Chat Interface**: Natural language interaction for car recommendations
- **Advanced Filtering**: Sophisticated car search based on multiple parameters
- **Database Integration**: PostgreSQL with SQLAlchemy ORM and async support
- **Caching**: Redis integration for improved performance
- **Background Tasks**: Support for Celery workers
- **Docker Support**: Containerized deployment with docker-compose
- **API Documentation**: Automatic OpenAPI/Swagger documentation

## Tech Stack

- **Backend**: FastAPI (Python 3.11+)
- **Database**: PostgreSQL with SQLAlchemy 2.0
- **Caching**: Redis
- **Authentication**: JWT tokens with bcrypt password hashing
- **ORM**: SQLAlchemy 2.0 with async support
- **Migration**: Alembic
- **Containerization**: Docker & docker-compose

## Project Structure

```
car_advisor/
├── app/
│   ├── api/
│   │   └── routers/          # API route definitions
│   ├── core/                 # Core application components
│   ├── db/                   # Database session management
│   ├── models/               # SQLAlchemy models
│   ├── repositories/         # Repository layer
│   ├── services/             # Business logic layer
│   ├── schemas/              # Pydantic schemas
│   ├── utils/                # Utility functions
│   └── main.py              # Application entry point
├── alembic/                 # Database migrations
├── logs/                    # Log files
├── requirements.txt         # Python dependencies
├── Dockerfile              # Docker configuration
├── docker-compose.yml      # Multi-container orchestration
├── .env                   # Environment variables
└── README.md              # This file
```

## Installation

### Prerequisites

- Python 3.11+
- PostgreSQL
- Redis
- Docker and Docker Compose (optional, for containerized deployment)

### Local Development Setup

1. Clone the repository:
```bash
git clone <repository-url>
cd car-advisor
```

2. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Set up environment variables:
```bash
cp .env.example .env
# Edit .env with your configuration
```

5. Run database migrations:
```bash
alembic upgrade head
```

6. Populate the database with sample car data:
```bash
python populate_cars.py
```

7. Start the application:
```bash
uvicorn app.main:app --reload
```

### Docker Setup

1. Build and start the containers:
```bash
docker-compose up --build
```

2. The API will be available at `http://localhost:8000`
3. API documentation will be available at `http://localhost:8000/docs`

## API Endpoints

### Authentication
- `POST /api/v1/register` - Register a new user
- `POST /api/v1/login` - Login and get JWT tokens
- `GET /api/v1/me` - Get current user info

### User Profile
- `GET /api/v1/profile` - Get user profile
- `PUT /api/v1/profile` - Update user profile
- `DELETE /api/v1/profile` - Delete user account

### Cars
- `GET /api/v1/cars` - Get all cars
- `GET /api/v1/cars/{id}` - Get car by ID
- `POST /api/v1/cars` - Create a new car (admin only)
- `PUT /api/v1/cars/{id}` - Update car (admin only)
- `DELETE /api/v1/cars/{id}` - Delete car (admin only)
- `GET /api/v1/cars/search/{query}` - Search cars by query

### Chat
- `POST /api/v1/chat/send` - Send a message to the car advisor
- `GET /api/v1/chat/sessions` - Get user's chat sessions
- `GET /api/v1/chat/sessions/{session_id}/messages` - Get messages from a session

## Environment Variables

The application requires the following environment variables:

- `DATABASE_URL`: PostgreSQL connection string
- `REDIS_URL`: Redis connection string
- `SECRET_KEY`: Secret key for JWT signing (at least 32 characters)
- `ACCESS_TOKEN_EXPIRE_MINUTES`: Access token expiration time
- `REFRESH_TOKEN_EXPIRE_DAYS`: Refresh token expiration time
- `DB_ECHO`: Enable/disable SQL query logging (true/false)
- `DB_POOL_SIZE`: Database connection pool size
- `DB_MAX_OVERFLOW`: Maximum database connections overflow
- `LOG_LEVEL`: Logging level (DEBUG, INFO, WARNING, ERROR)

## Security

- Passwords are hashed using bcrypt
- JWT tokens with configurable expiration
- Input validation using Pydantic schemas
- SQL injection prevention through SQLAlchemy ORM
- Rate limiting capabilities (implementation pending)

## Background Tasks with Celery

The application includes support for background tasks using Celery with Redis as a message broker.

### Running Celery Worker

To run the Celery worker locally:

1. Make sure Redis is running
2. Activate your virtual environment
3. Run the Celery worker:
```bash
celery -A app.celery_app worker --loglevel=info
```

Alternatively, you can use the provided script:
```bash
# On Unix/Linux/MacOS:
./start_celery.sh

# On Windows:
start_celery.bat
```

### Using Background Tasks

The application exposes endpoints to trigger background tasks:

- `POST /celery/send-email/` - Queue an email sending task
- `POST /celery/process-car-data/` - Queue a car data processing task
- `GET /celery/task-status/{task_id}` - Check the status of a queued task

Example request to queue an email task:
```json
{
  "email": "user@example.com",
  "subject": "Test Subject",
  "body": "Test Body"
}
```

### Docker Setup

When using Docker Compose, the Celery worker runs automatically as part of the stack:
```bash
docker-compose up --build
```

## Testing

Run unit tests:
```bash
pytest tests/
```

Run with coverage:
```bash
pytest --cov=app tests/
```

## Deployment

For production deployment:

1. Use the provided `docker-compose.yml` with production-grade configurations
2. Set up SSL certificates for HTTPS
3. Configure a reverse proxy (nginx recommended)
4. Set up a proper PostgreSQL instance (not the development one)
5. Use a production WSGI server like Gunicorn instead of uvicorn in development mode

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.