import praw
import csv
import pandas as pd
import os
import re
import nltk
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer
from transformers import BertTokenizer
from dotenv import load_dotenv
from langdetect import detect, LangDetectException,DetectorFactory

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
    comments = []
    for comment in subreddit.comments(limit=limit):
        comments.append({"comment_id": comment.id,
                         "comment_body": comment.body
                            , "created_utc": comment.created_utc})

    if not comments:
        print(f"Failed to fetch comments from the subreddit r/{subreddit_name}")
        return []
    fieldnames = ['comment_id', 'created_utc', 'comment_body']

    # Save comments to CSV file
    # "w" mode creates the file if it doesn't exist and truncates/overwrites it if it does exist
    with open(filename, "w", newline="", encoding="utf-8") as comment_file:
        writer = csv.DictWriter(comment_file, delimiter=",", fieldnames=fieldnames)
        writer.writeheader()
        for comment in comments:
            writer.writerow(comment)
    print(f"Saved {len(comments)} comments to {filename}")
    return [item['comment_body'] for item in comments]



def clean_up_data(filename: str,clean_file: str):
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





fetch_reddit_comments("comments.csv", subreddit_name="csMajors", limit=20)
clean_up_data("comments.csv","cleaned_comments.csv")



