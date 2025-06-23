from flask import Flask, request, jsonify
from transformers import BertTokenizer
from reddit_sentiment_pipeline.data.raw.reddit_fetcher import clean_text_for_bert
from reddit_sentiment_pipeline.src.modeling.model_utils import tokenizer, tokenize_data
app = Flask(__name__)
import datetime

@app.route('/')
def welcome():
    print(f"{datetime.datetime.now()}")
    return f'Welcome to the Reddit Sentiment Pipeline'
@app.route('/predict',methods=['POST'])
def predict():
    # 1. Get the JSON data.
    json_data = request.get_json()

    # --- GUARD CLAUSES ---

    # Guard 1: Check if any JSON was sent at all.
    if not json_data:
        return jsonify({"error": "Invalid input: No JSON data received."}), 400

    # Guard 2: Check if the 'text' key is missing from the JSON.
    if 'text' not in json_data:
        return jsonify({"error": "Invalid input: Missing 'text' key in JSON."}), 400

    # Guard 3: Check if the 'text' value is valid (not empty after stripping whitespace).
    text_value = json_data['text']
    if not isinstance(text_value, str) or not text_value.strip():
        return jsonify({"error": "Invalid input: 'text' field cannot be empty."}), 400

    # --- If we pass all the guards, we're good to go! ---

    print(f"Received valid text for processing: '{text_value}'")

    clean_data = clean_text_for_bert(text_value)
    tokenized_data = tokenize_data(clean_data)
    print(f"Received tokenized data for processing: '{tokenized_data}'")
    print("Generating dummy predictions")
    dummy_prediction = "positive"
    confidence = 0.99


# For now, we'll return a success message.
    return jsonify({
    "message": "Data received successfully",
    "prediction": text_value,
    "confidence": confidence
}), 200





if __name__ == '__main__':
    app.run(debug=True)
