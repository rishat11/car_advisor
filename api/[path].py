import os
import sys
from mangum import Mangum
from app.main import app

# Для Vercel Serverless Functions нужен экспорт handler
handler = Mangum(app, lifespan="off")