import pandas as pd
from news_cleaner.src.cleaner import clean_dataframe
from news_cleaner.src.analyser import analyse_dataframe
from pathlib import Path

RAW_PATH = Path("data/raw/news_articles.csv")
PROCESSED_PATH = Path("data/raw/cleaned_articles.csv")

def main():
    print("Starting cleaning and analysis")

    df = pd.read_csv(RAW_PATH)

    df = clean_dataframe(df)
    df = analyse_dataframe(df)

    PROCESSED_PATH.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(PROCESSED_PATH, index=False)
    print("Saved clean file")

if __name__ == "__main__":
    main()

                  