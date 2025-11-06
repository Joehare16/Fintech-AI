##use text blob library to get some initial insights

from textblob import TextBlob
import pandas as pd
from typing import List

def analyse_sentiment(text:str) -> List[float]:
    if not isinstance(text, str) or not text.strip():
        return 0.0, 0.0
    s = TextBlob(text).sentiment
    return s.polarity, s.subjectivity

def analyse_POS(text, tag_prefix):
    if not isinstance(text, str) or not text.strip(): return 0
    tags = TextBlob(text).tags
    return sum(1 for _, tag in tags if tag.startswith(tag_prefix)) / len(tags)

def analyse_dataframe(df: pd.DataFrame) -> pd.DataFrame:
    # add the sentiment scores to the dataframe

    print("Analysing")
    df[["sentiment_polarity", "sentiment_subjectivity"]] = df["content"].apply(analyse_sentiment).apply(pd.Series)
    df["noun_phrases"] = df["content"].apply(lambda text: TextBlob(text).noun_phrases if isinstance(text,str) else [])
    df["word_count"] = df["content"].apply(lambda text: len(TextBlob(text).words) if isinstance(text,str) else 0)
    df["adj_ratio"] = df["content"].apply(lambda text: analyse_POS(text, "JJ")) 
    df["verb_ratio"] = df["content"].apply(lambda text: analyse_POS(text, "VB"))
    print("analysis complete added to dataframe")

    return df

