import praw
import csv
import pandas as pd
import emoji
import os
import nltk
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer
from transformers import BertTokenizer
from dotenv import load_dotenv
from langdetect import detect, LangDetectException,DetectorFactory
import re

reddit = praw.Reddit(
    client_id="mzLyRMCgSUkgRamThw6msg",
    client_secret="OOVynNKSC0MD55ATz7K7zGBORI-KfA",
    password="Lukondeh@20262027",
    user_agent="script:RealTimeSentimentAnalysis:v0.1 (by /u/Suspicious-Week-5144)",
    username="Suspicious-Week-5144",
)
print("Reddit client initialized successfully.")
print(reddit.user.me())


def fetch_reddit_comments(filename: str, subreddit_name: str, limit: int):
    """
    Fetches comments from a specified subreddit.

    Args:
        subreddit_name (str): The name of the subreddit to fetch comments from.
        limit (int): The maximum number of comments to fetch.

    Returns:
        list: A list of comments fetched from the subreddit.
        :param limit:
        :param subreddit_name:
        :param filename:
    """
    subreddit = reddit.subreddit(subreddit_name)
    comments_data = []
    for comment in subreddit.comments(limit=limit):
        comments_data.append({"comment_id": comment.id,
                         "comment_body": comment.body
                            , "created_utc": comment.created_utc})

    if not comments_data:
        print(f"Failed to fetch comments from the subreddit r/{subreddit_name}")
        return []
    fieldnames = ['comment_id', 'created_utc', 'comment_body']

    # Save comments to CSV file
    # "w" mode creates the file if it doesn't exist and truncates/overwrites it if it does exist
    with open(filename, "w", newline="", encoding="utf-8") as comment_file:
        writer = csv.DictWriter(comment_file, delimiter=",", fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(comments_data)
    print(f"Saved {len(comments_data)} comments to {filename}")
    return [item['comment_body'] for item in comments_data]



def process_and_clean_data(filename: str, clean_file: str):
    """"""
    df = pd.read_csv(filename)
    df.dropna(subset=['comment_body'],inplace=True)
    # The line below filters out rows where the comment_body column is empty or contains only whitespace.
    # It keeps only rows where comment_body is not an empty string after stripping spaces.
    df = df[df['comment_body'].str.strip() != ""]
    df = add_language_column(df)
    df.to_csv(clean_file,index=False)



def add_language_column(df):
    DetectorFactory.seed = 0
    try:
        df['language'] = df['comment_body'].apply(lambda x: detect(x) if pd.notnull(x) and x.strip() != "" else "unknown")
    except LangDetectException:
        df['language'] = "unknown"
    return df


def filter_english_comments(csv: str):
    """"""
    df = pd.read_csv(csv)
    # using boolean indexing, I can figure out if language == 'en':
    # make a new column that will only include comments with english
    is_english_mask = (df['language'] == "en")
    english_df = df[is_english_mask].copy()
    print(f"Number of English comments found: {len(english_df)}")

    return english_df


def clean_text_for_bert(text: str) -> str:
    """
    Performs a series of cleaning steps on a text string to prepare it for a
    BERT model.
    """
    if not isinstance(text, str):
        return ""

    # 1. Lowercase the text
    text = text.lower()

    # 2. Remove URLs, emails, and HTML entities
    text = re.sub(r'https?://\S+|www\.\S+|\S+@\S+\.\S+', ' ', text)
    text = re.sub(r'&[a-zA-Z]+;', ' ', text)

    # 3. Remove mentions and hashtags
    text = re.sub(r'@\w+|#\w+', ' ', text)

    # 4. Remove emojis
    # The replace='' argument removes the emoji characters completely.
    text = emoji.replace_emoji(text, replace='')

    # 5. Handle Punctuation (Nuanced for BERT)
    # This is the key addition. We remove characters that are NOT letters,
    # numbers, spaces, or apostrophes. We replace them with a space.
    text = re.sub(r"[^a-zA-Z0-9' ]", " ", text)

    # 6. Normalize whitespace
    # This combines multiple spaces into one and removes leading/trailing spaces.
    text = " ".join(text.split())


    return text

if __name__ == "__main__":

    english_df = filter_english_comments("cleaned_comments.csv")
    print("\nApplying BERT-specific cleaning to English comments...")
    english_df['cleaned_body'] = english_df['comment_body'].apply(clean_text_for_bert)

    print("\nSample of final cleaned data:")
    print(english_df[['comment_body', 'cleaned_body']].sample(5))
    FINAL_FILENAME = "final_cleaned_data.parquet"
    print(f"\nSaving final cleaned data to {FINAL_FILENAME}...")
    # Using .parquet is often more efficient for DataFrames
    english_df.to_parquet(FINAL_FILENAME, index=False)
    print("Done!")
