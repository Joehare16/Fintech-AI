# run fetch - clean - save 
import logging
from news_fetcher.fetcher import fetch_news

from .config import RAW_DATA_FILE

logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")

if __name__ == "__main__":
    fetch_news(query="technology",days_back=4)
    logging.info("News fetching completed. Articles stored in database.")