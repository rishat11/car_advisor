import os
import sys
from app.main import app

# Для Vercel нужно экспортировать приложение как 'app'
# Это позволяет Vercel правильно распознать ASGI приложение
handler = app