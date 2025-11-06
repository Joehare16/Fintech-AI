import pandas as pd 
import re
from bs4 import BeautifulSoup

def clean_text(text:str) -> str:
    # remove any white spaces etc unwatned characters from our data

    if pd.isna(text):
        return ""
    
    #remove any html text
    text = BeautifulSoup(text, "html.parser").get_text()
    text = re.sub(r"\s+", " ", text)

    return text.strip()

def clean_dataframe(df: pd.DataFrame) -> pd.DataFrame:
    print("Performing cleaning")

    df = df.drop_duplicates(subset = ["title","content"])
    df = df.dropna(subset = ["title","content"])

    df["title"] = df["title"].apply(clean_text)

    df["content"] = df["content"].apply(clean_text)
    df["description"] = df["description"].apply(clean_text)

    # Normalize casing
    df["title"] = df["title"].str.strip()
    df["content"] = df["content"].str.strip()

    print("Cleaning complete")

    return df