# gets the news from apis and web scraping
import logging
import time 
from datetime import datetime, timedelta
from typing import List, Dict, Optional

import os 
import psycopg2

import pandas as pd
import requests
from tenacity import retry, stop_after_attempt, wait_exponential, retry_if_exception_type

from .config import NEWS_API_KEY, BASE_URL

logger = logging.getLogger(__name__)

DEFAULT_TIMEOUT = 10 # seconds 
DEFAULT_MAX_PAGES = 5
PAGE_SIZE = 20 # max for newsapi

QUERY_KEYWORDS = "(stock OR stocks OR shares OR equity OR earnings OR revenue OR profit OR guidance OR investors OR market OR markets OR Wall Street OR IPO OR acquisition OR merger OR takeover OR hedge fund OR asset manager OR portfolio)"
DOMAIN_SOURCES = ("bloomberg.com,techcrunch.com,reuters.com,wsj.com,financialpost.com,ft.com,cnbc.com,marketwatch.com,investopedia.com,seekingalpha.com,theverge.com,theinformation.com")

try: 
    conn = psycopg2.connect(
        host = os.getenv("HOST", "localhost"),
        user = os.getenv("POSTGRES_USER", "postgres"),
        password = os.getenv("POSTGRES_PASSWORD", "postgres"),
        dbname = os.getenv("POSTGRES_DB", "FintechAI"),
        port = 5432)
    print("Database connection established.")
except Exception as e:
        print("Error connecting to database: %s", e)

cur = conn.cursor()



class FetcherError(Exception):
    pass

def _default_headers():
    #sends back our app to the remote server
    return {
        "User-Agent": "TechTrendsAI/0.1 (+https://github.com/JoeHare16/techtrends-ai)"
    }


    #details when we should recall the api if it fails
@retry(
        retry=retry_if_exception_type((requests.exceptions.RequestException, FetcherError)),
        #extends how long we wait to do an api recall up to 60 seconds
        wait=wait_exponential(multiplier = 1, min=2, max=60),
        #stop after 5 attempts
        stop=stop_after_attempt(5),
        reraise=True, # if all fail raise
)

#make the get request
def _do_get(url: str, params: dict, timeout: int = DEFAULT_TIMEOUT) -> dict:
    headers = _default_headers()
    resp = requests.get(url, params=params, headers=headers, timeout=timeout)

    #rate limiting
    #error  429 means too many requests
    if resp.status_code == 429:
        retry_after = resp.headers.get("Retry-After")
        if retry_after:
            wait = int(retry_after)
            logger.warning("Rate limited; sleeping for %s seconds", wait)
            time.sleep(wait)
        raise FetcherError("Rate limited by remote API (429).")
    try:
        resp.raise_for_status()
    except requests.exceptions.HTTPError as e:
        # for 4xx other than 429, don't retry too many times, but we allow the retry wrapper to handle attempts
        logger.error("HTTP error from %s: %s - body: %s", url, e, resp.text[:300])
        raise
    return resp.json()

# now we need to normalise this data to a consistent format we can store

def _normalize_newsapi_article(raw_article:dict) -> dict:


    return {
        "source":str(raw_article.get("source", {}).get("name") if isinstance(raw_article.get("source"), dict) else raw_article.get("source")),
        "author": str(raw_article.get("author")),
        "title": str(raw_article.get("title")),
        "description": str(raw_article.get("description")),
        "url": str(raw_article.get("url")),
        "published_at": str(raw_article.get("publishedAt")),
        "content": str(raw_article.get("content")),
        "raw" : raw_article,
    }

def insert_articles_to_db(cur, articles: List[dict]):
    try:
        for article in articles: 
            cur.execute(
            """INSERT INTO articles(source,author,title,description,url, published_at, content)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
            """,
            (
                article["source"],
                article["author"],
                article["title"],
                article["description"],
                article["url"],
                article["published_at"],
                article["content"]
            ),
        )
    except Exception as e:
            logger.error("Database insert failed: %s", e)

# call the do_get function to get the newsapi data page by page, supply the args for the api call
#pages - if we want 200 articles each page is 50 therefore we need 4 page / apis calls
def _fetch_newsapi_page(query: str, domains: str, language: str, from_date: Optional[str], page: int, page_size: int) -> List[dict]:

    #sets parameters for the api call
    params = {
        "q": query,
        "domains": domains,
        "language": language,
        "page": page,
        "pageSize": page_size,
        "apiKey": NEWS_API_KEY,
    }
    #include date if provided
    if from_date:
        params["from"] = from_date
    
    #debug that were making a call with these parametes
    logger.debug("Fetching NewsAPI page %s with params: %s", page, {k: v for k,v in params.items() if k != "apiKey"})
    data = _do_get(BASE_URL, params)
    articles = data.get("articles", [])
    return [_normalize_newsapi_article(article) for article in articles]


def fetch_news(query: str = QUERY_KEYWORDS,
    domains: str = DOMAIN_SOURCES,
    language: str = "en",
    days_back: int = 1,
    page_size: int = PAGE_SIZE,
    max_pages: int = DEFAULT_MAX_PAGES,
) -> pd.DataFrame:
    
    from_date = (datetime.utcnow() - timedelta(days=days_back)).strftime("%Y-%m-%dT%H:%M:%SZ")
    collected = []
    for page in range(1 , max_pages + 1):
        try:
            page_items = _fetch_newsapi_page(query,domains,language,from_date, page, page_size)
        except Exception as e:
            logger.error("Error fetching page %s: %s", page, e)
            break
        if not page_items:
            logger.info("No more articles found, stopping at page %s", page)
            break
        collected.extend(page_items) #adds these new    articles to the collected list
        logger.info("Fetched %s articles from page %s", len(page_items), page)

        logger.info("attempting to store in database")
        try:
            insert_articles_to_db(cur, page_items)
            conn.commit()
            logger.info("Successfully inserted page %s into the DB", page)
        except Exception as e:
            logger.error("Failed to insert page %s into the DB due to error %s", (page, e))
            continue
        if len(page_items)  < page_size:
            logger.info("Fewer articles than page size (%s) on page %s, stopping.", page_size, page)
            break

    df = pd.DataFrame(collected)
    df["published_at"] = pd.to_datetime(df["published_at"], errors="coerce")
    df = df.drop_duplicates(subset=["url"])
    df = df.dropna(subset=["url","title"])
    logger.info("Total articles fetched: %s", len(df))
    return df

    
