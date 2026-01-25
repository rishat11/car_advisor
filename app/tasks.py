from app.celery_app import celery_app
import time


@celery_app.task
def send_email_task(email: str, subject: str, body: str):
    """
    Пример задачи Celery для отправки email
    """
    # Симуляция процесса отправки email
    time.sleep(5)  # Имитация задержки
    print(f"Отправка email на {email} с темой '{subject}' и телом '{body}'")
    return {"status": "Email sent successfully", "to": email}


@celery_app.task
def process_car_data_task(car_id: int):
    """
    Пример задачи Celery для обработки данных автомобиля
    """
    # Симуляция обработки данных автомобиля
    time.sleep(3)  # Имитация задержки
    print(f"Обработка данных для автомобиля с ID {car_id}")
    return {"status": "Car data processed", "car_id": car_id}