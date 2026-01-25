import os
import sys
from mangum import Mangum
from app.main import app

# Для Vercel нужно правильно обернуть FastAPI приложение в Mangum
# Это позволяет Vercel распознать наше приложение как ASGI-совместимое
handler = Mangum(app, lifespan="off")

# Также убедимся, что в serverless среде не используется lifespan
# потому что подключение к БД будет происходить при каждом вызове