from mangum import Mangum
from app.main import app

# Create the handler for Vercel
handler = Mangum(app, lifespan="off")