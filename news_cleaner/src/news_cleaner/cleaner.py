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
    
    noise_words = [] # remove common words that add no value.

    for col in ["title", "content","description"]:
        
        if col in df.columns:
            df[col] = df[col].apply(clean_text)

            #for word in noise_words:
                #df[col] = df[col].str.replace(rf"\b{re.escape(word)}\b", "", regex=True)
        else:
            df[col] = ""

    df = df.replace("", pd.NA)
    df = df.dropna(how="all",subset = ["title","content"])

    # Normalize casing
    df["title"] = df["title"].str.strip().str.lower()
    df["content"] = df["content"].str.strip().str.lower()
    df["description"] = df["description"].str.strip().str.lower()
    

    df = df.drop_duplicates(subset=["title", "content"], keep="first")
    if "content" in df.columns:
        df = df.drop_duplicates(subset=["content"], keep="first")

    print("Cleaning complete")

    return df