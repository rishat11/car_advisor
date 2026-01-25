#!/bin/bash
# Скрипт для запуска Celery вручную для тестирования

export $(grep -v '^#' .env | xargs)

celery -A app.celery_app worker --loglevel=info