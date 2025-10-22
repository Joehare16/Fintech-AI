# run fetch - clean - save 
import logging
from news_fetcher.fetcher import fetch_news

logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")

if __name__ == "__main__":
    df = fetch_news(query="technology",days_back=4)
    print(df.head())
    print(f"/n Successfully fetched {len(df)} articles.")
    df.to_csv("data/raw/news_articles.csv", index=False)
    print("\n✅ Saved to data/raw/news_articles.csv")