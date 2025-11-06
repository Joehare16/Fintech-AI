#loads configurations from the .env file
import os
from dotenv import load_dotenv

load_dotenv()

NEWS_API_KEY = os.getenv("NEWS_API_KEY", "6522474117e344209e52456e4aea0322")
BASE_URL = os.getenv("BASE_URL", "https://newsapi.org/v2/everything")

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..",".."))
BASE_DATA_DIR = os.getenv("DATA_DIR", os.path.join(BASE_DIR,"data"))
RAW_DATA_DIR = os.path.join(BASE_DATA_DIR, "raw")
RAW_DATA_FILE = os.path.join(RAW_DATA_DIR, "news_articles.csv")