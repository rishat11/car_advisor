# Этот файл создан для совместимости с существующей конфигурацией docker-compose.yml
# Он импортирует основное приложение Celery из celery_app.py

from app.celery_app import celery_app

# Экспортируем приложение Celery под именем worker для совместимости
worker = celery_app