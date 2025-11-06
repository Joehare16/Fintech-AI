import pandas as pd
from news_cleaner.cleaner import clean_dataframe
from news_cleaner.analyser import analyse_dataframe
from pathlib import Path

from .config import CLEANED_DATA_FILE, CLEANED_DATA_DIR, RAW_DATA_FILE

def main():
    print("Starting cleaning and analysis")

    df = pd.read_csv(RAW_DATA_FILE)

    df = clean_dataframe(df)
    df = analyse_dataframe(df)

    CLEANED_DIR = Path(CLEANED_DATA_DIR)

    CLEANED_FILE = Path(CLEANED_DATA_FILE)
    
    CLEANED_DIR.mkdir(parents=True, exist_ok=True)
    df.to_csv(CLEANED_FILE, index=False)
    print("Saved clean file")

if __name__ == "__main__":
    main()

                  