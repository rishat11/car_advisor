@echo off
rem Скрипт для запуска Celery вручную для тестирования

setlocal

for /f "tokens=*" %%i in ('type .env ^| findstr /v "^#"') do (
    for /f "tokens=1,* delims==" %%j in ("%%i") do (
        set "%%j=%%k"
    )
)

python -m celery -A app.celery_app worker --loglevel=info