import praw
import csv
import pandas as pd
import os
import re
import nltk
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer
from transformers import BertTokenizer
from langdetect import detect, LangDetectException

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
    # "w" handles the exception if a file does not exist
    with open(filename, "w", newline="", encoding="utf-8") as comment_file:
        writer = csv.DictWriter(comment_file, delimiter=",", fieldnames=fieldnames)
        writer.writeheader()
        for comment in comments:
            writer.writerow(comment)
    print(f"Saved {len(comments)} comments to {filename}")
    return [item['comment_body'] for item in comments]


# def get_comment_language(text_comment):
#     """
#     Detects the language of a single text comment.
#     Returns the language code (e.g., 'en') or 'unknown' if detection fails.
#     """
#     try:
#         # Ensure the input is a string, handle potential NaN or other types
#         if not isinstance(text_comment, str) or pd.isna(text_comment):
#             return "unknown"
#         if not text_comment.strip():  # Handle empty or whitespace-only strings
#             return "unknown"
#         return detect(text_comment)
#     except LangDetectException:
#         return "unknown"  # Or any other placeholder for errors/undetectable
#
#
# def clean_up_data(csvfile, new_csv):
#     return


fetch_reddit_comments("comments.csv", subreddit_name="quant", limit=10)
