import pandas as pd
import logging
from news_cleaner.cleaner import clean_dataframe
from news_cleaner.analyser import analyse_dataframe
from news_cleaner.companytagger import tag_companies
from pathlib import Path

import json 

import os 
import psycopg2

from .config import CLEANED_DATA_FILE, CLEANED_DATA_DIR, RAW_DATA_FILE

def main():
    logger = logging.getLogger(__name__)
    logger.info("Starting database connection")
    try: 
        conn = psycopg2.connect(
            host = os.getenv("HOST", "localhost"),
            user = os.getenv("POSTGRES_USER", "postgres"),
            password = os.getenv("POSTGRES_PASSWORD", "postgres"),
            dbname = os.getenv("POSTGRES_DB", "FintechAI"),
            port = 5432)
        logger.info("Database connection established.")
    except Exception as e:
        logger.error("Error connecting to database: %s", e)
        return
    cur = conn.cursor()

    logger.info("Fetcher Articles from database")

    try:
        cur.execute("SELECT source, author, title, description, url, published_at, content, fetched_at FROM articles;")
        rows = cur.fetchall()
        df = pd.DataFrame(rows, columns=["source", "author", "title", "description", "url", "published_at", "content","fetched_at"])
        logger.info("Fetched %d articles from database", len(df))
    except Exception as e:
        logger.error("Error fetching articles from database: %s", e)
        return
    logger.info("Starting cleaning and analysis")

    df = clean_dataframe(df)
    df = analyse_dataframe(df)
    df = tag_companies(df)


    logger.info("Attempting to insert clean articles")
    for _, row in df.iterrows():
            try:
                
                if row["noun_phrases"] is not None:
                     row["noun_phrases"] = json.dumps(row["noun_phrases"])

                cur.execute("""INSERT INTO cleaned_articles(
                            source,
                            author,
                            title,
                            description,
                            url,
                            published_at,
                            content,
                            fetched_at,
                            sentiment_polarity,
                            sentiment_subjectivity,
                            adj_ratio,
                            verb_ratio,
                            word_count,
                            noun_phrases
                        )     VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
                        """, (
                            row["source"],
                            row["author"],
                            row["title"],
                            row["description"],
                            row["url"],
                            row["published_at"],
                            row["content"],
                            row["fetched_at"],
                            row["sentiment_polarity"],
                            row["sentiment_subjectivity"],
                            row["adj_ratio"],
                            row["verb_ratio"],
                            row["word_count"],
                            row["noun_phrases"]
                        ))
                conn.commit()
                logger.info("Successfully inserted clean articles")
            except Exception as e:
                logger.error("Database insert failed: ",e)
                conn.rollback()
if __name__ == "__main__":
    main()

                  