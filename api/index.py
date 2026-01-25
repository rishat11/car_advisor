from app.main import app
from mangum import Mangum

# Оборачиваем FastAPI приложение для AWS Lambda
handler = Mangum(app)