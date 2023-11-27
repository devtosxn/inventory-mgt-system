import datetime
import os

from dotenv import load_dotenv

load_dotenv()

SECRET_KEY = os.getenv("SECRET_KEY")
MONGO_URI = os.getenv("MONGO_DB_URI")

# JWT
JWT_TOKEN_TTL_HOURS = 24
JWT_ACCESS_TOKEN_EXPIRES = datetime.timedelta(hours=JWT_TOKEN_TTL_HOURS)
