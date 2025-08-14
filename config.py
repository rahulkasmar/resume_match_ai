# config.py
import os
from dotenv import load_dotenv
from datetime import timedelta

# Load variables from .env file
load_dotenv()

# MongoDB
MONGO_URI = os.getenv("MONGO_URI")

# JWT
JWT_SECRET = os.getenv("JWT_SECRET")
JWT_ALGORITHM = os.getenv("JWT_ALGORITHM", "HS256")
JWT_EXPIRATION = timedelta(minutes=int(os.getenv("JWT_EXPIRATION_MINUTES", 30)))

# Groq API
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
