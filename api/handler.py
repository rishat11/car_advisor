from mangum import Mangum
from . import app  # Import from the index.py file

handler = Mangum(app, lifespan="off")