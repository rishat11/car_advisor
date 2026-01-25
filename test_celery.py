"""
Тестовый файл для проверки работы Celery
"""

import requests
import uuid
import os

BASE_URL = os.getenv("BACKEND_URL", "http://localhost:8000")


def test_celery_integration():
    """Тестирует интеграцию с Celery через API-эндпоинты"""
    
    # Тест 1: Отправка задачи на отправку email
    print("Тест 1: Отправка задачи на отправку email...")
    email_payload = {
        "email": f"user_{uuid.uuid4()}@example.com",
        "subject": "Тестовое сообщение",
        "body": "Это тестовое сообщение из системы Car Advisor"
    }
    
    try:
        response = requests.post(f"{BASE_URL}/celery/send-email/", json=email_payload)
        if response.status_code == 200:
            result = response.json()
            task_id = result['task_id']
            print(f"  Задача успешно поставлена в очередь: {task_id}")
            
            # Проверяем статус задачи
            print("  Проверяем статус задачи...")
            status_response = requests.get(f"{BASE_URL}/celery/task-status/{task_id}")
            if status_response.status_code == 200:
                status_result = status_response.json()
                print(f"  Статус задачи: {status_result['status']}")
                print(f"  Результат: {status_result['result']}")
            else:
                print(f"  Ошибка получения статуса задачи: {status_response.status_code}")
        else:
            print(f"  Ошибка отправки задачи: {response.status_code}")
    except Exception as e:
        print(f"  Ошибка при тестировании отправки email: {e}")
    
    print()
    
    # Тест 2: Отправка задачи на обработку данных автомобиля
    print("Тест 2: Отправка задачи на обработку данных автомобиля...")
    car_data_payload = {
        "car_id": 1
    }
    
    try:
        response = requests.post(f"{BASE_URL}/celery/process-car-data/", json=car_data_payload)
        if response.status_code == 200:
            result = response.json()
            task_id = result['task_id']
            print(f"  Задача успешно поставлена в очередь: {task_id}")
            
            # Проверяем статус задачи
            print("  Проверяем статус задачи...")
            status_response = requests.get(f"{BASE_URL}/celery/task-status/{task_id}")
            if status_response.status_code == 200:
                status_result = status_response.json()
                print(f"  Статус задачи: {status_result['status']}")
                print(f"  Результат: {status_result['result']}")
            else:
                print(f"  Ошибка получения статуса задачи: {status_response.status_code}")
        else:
            print(f"  Ошибка отправки задачи: {response.status_code}")
    except Exception as e:
        print(f"  Ошибка при тестировании обработки данных автомобиля: {e}")


if __name__ == "__main__":
    print("Запуск тестов интеграции Celery...")
    print("=" * 50)
    
    test_celery_integration()
    
    print("=" * 50)
    print("Тестирование завершено.")