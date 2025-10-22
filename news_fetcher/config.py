#loads configurations from the .env file
import os
from dotenv import load_dotenv

load_dotenv()

NEWS_API_KEY = os.getenv("NEWS_API_KEY", "6522474117e344209e52456e4aea0322")
BASE_URL = os.getenv("BASE_URL", "https://newsapi.org/v2/everything")