from nltk import sentiment
from transformers import BertTokenizer
import torch
from transformers import pipelines as pipe
print("Loading Sentiment Model.....")
sentiment_pipeline = pipe.pipeline("sentiment-analysis", model="cardiffnlp/twitter-roberta-base-sentiment-latest")
print("Model loaded!")
def analyze_sentiment(text: str):
    print("Analyzing sentiment.....")
    result  = sentiment_pipeline(text)
    print(result)

analyze_sentiment("I hate this project")
analyze_sentiment("This is okay I guess")
analyze_sentiment("Amazing work!")
analyze_sentiment("Not sure how I feel")

import time

# Test single vs batch processing
texts = ["I love this!", "This is terrible", "Okay experience", "Amazing work!"]

# Method 1: One by one
start = time.time()
results1 = [sentiment_pipeline(text) for text in texts]
time1 = time.time() - start

# Method 2: All at once
start = time.time()
results2 = sentiment_pipeline(texts)
time2 = time.time() - start

print(f"One by one: {time1:.3f} seconds")
print(f"Batch: {time2:.3f} seconds")