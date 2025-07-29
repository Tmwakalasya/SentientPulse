from flask import Flask, request, jsonify
import pandas as pd
import datetime
import os
app = Flask(__name__)

def load_file(filepath: str):
    try:
        if os.path.exists(filepath):
            print("Loading the file.....")
            df = pd.read_parquet(filepath)
            print(f"Length of dataframe: {len(df)}")
            return df
        else:
            print("File not found...")
            return None
    except Exception as e:
        print(f"Failed to load file: {e}")
        return None


@app.route('/')
def welcome():
    print(f"{datetime.datetime.now()}")
    return f'Welcome to the Reddit Sentiment Pipeline'
@app.route('/summary',methods=['GET'])
def get_summary():
    pass

@app.route('/comments',methods=['GET'])
def get_comments():
    pass
@app.route('/positive',methods=['GET'])
def positive_comments():
    pass
@app.route('/negative',methods=['GET'])
def negative_comments():
    pass

if __name__ == '__main__':
    load_file("final_cleaned_data.parquet")
    app.run(debug=True)