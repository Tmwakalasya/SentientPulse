from flask import Flask, request, jsonify
from transformers import BertTokenizer
from reddit_sentiment_pipeline.data.raw.reddit_fetcher import clean_text_for_bert
app = Flask(__name__)
import datetime

@app.route('/')
def welcome():
    print(f"{datetime.datetime.now()}")
    return f'Welcome to the Reddit Sentiment Pipeline'
@app.route('/predict',methods=['POST'])
def predict():
    pass





if __name__ == '__main__':
    app.run(debug=True)
