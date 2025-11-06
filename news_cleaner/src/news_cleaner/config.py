import os


BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..",".."))
BASE_DATA_DIR = os.getenv("DATA_DIR", os.path.join(BASE_DIR,"data"))
RAW_DATA_DIR = os.path.join(BASE_DATA_DIR, "raw")
RAW_DATA_FILE = os.path.join(RAW_DATA_DIR, "news_articles.csv")

CLEANED_DATA_DIR = os.path.join(BASE_DATA_DIR, "cleaned")
CLEANED_DATA_FILE = os.path.join(CLEANED_DATA_DIR, "cleaned_articles.csv")