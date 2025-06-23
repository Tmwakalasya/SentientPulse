# Reddit Sentiment Analysis Pipeline

This project is an end-to-end machine learning pipeline that fetches real-time data from Reddit, processes it, and uses a fine-tuned BERT model to perform sentiment analysis. The final model is exposed via a RESTful API.

## Project Goals
* Demonstrate a full ML pipeline from data ingestion to a deployed API.
* Utilize modern NLP techniques with Hugging Face Transformers.
* Build a robust, scalable, and well-documented web service.
* Implement CI/CD practices for automated testing and deployment.

## Tech Stack
* **Data Ingestion:** Python, PRAW (Python Reddit API Wrapper)
* **Data Processing:** Pandas, NumPy, NLTK, langdetect
* **Machine Learning:** PyTorch, Hugging Face (Transformers, Tokenizers)
* **API Service:** Flask
* **Containerization:** Docker
* **Deployment (Planned):** AWS (e.g., Elastic Beanstalk), GitHub Actions for CI/CD

## Project Structure
```
reddit_sentiment_pipeline/
├── api/
│   └── routes.py              # Flask application
├── data/
│   ├── raw/                # Raw data from Reddit
│   └── processed/          # Cleaned and tokenized data
├── notebooks/                # Jupyter notebooks for exploration
├── src/
│   ├── data_processing.py  # Scripts for cleaning and filtering
│   └── modeling/
│       ├── model_utils.py  # Tokenization and model prediction logic
│       └── train.py        # Script for model fine-tuning
├── tests/                    # Unit and integration tests
├── .gitignore
├── Dockerfile                # For the Flask API
├── praw.ini                  # API credentials (should be in .gitignore)
└── requirements.txt
```

## Setup & Installation

1.  **Clone the repository:**
    ```bash
    git clone [your-repo-url]
    cd reddit_sentiment_pipeline
    ```

2.  **Create and activate a virtual environment:**
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
    ```

3.  **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

4.  **Set up credentials:**
    * Create a `praw.ini` file in the root directory with your Reddit API credentials. Refer to the PRAW documentation for the correct format.

## Running the Application

### 1. Fetching Data
To fetch the latest comments from a subreddit:
```bash
python src/data_processing.py
```
*(You may want to refactor the main execution block into separate scripts later, e.g., `fetch_data.py`, `clean_data.py`)*

### 2. Running the API
To run the Flask development server:
```bash
# Make sure your terminal is in the project's root directory
export FLASK_APP=src.api.app  # On Windows, use `set FLASK_APP=src.api.app`
flask run
```
The server will be available at `http://127.0.0.1:5000`.

## API Usage

### `/predict`

This endpoint performs sentiment analysis on a given piece of text.

* **URL:** `/predict`
* **Method:** `POST`
* **Body (JSON):**
    ```json
    {
        "text": "Your text to be analyzed goes here. I am feeling very optimistic today!"
    }
    ```
* **Example `curl` Request:**
    ```bash
    curl -X POST \
      [http://127.0.0.1:5000/predict](http://127.0.0.1:5000/predict) \
      -H 'Content-Type: application/json' \
      -d '{"text": "This is a fantastic project and I am learning a lot."}'
    ```
* **Success Response (200):**
    ```json
    {
      "prediction": "Positive",
      "confidence_score": 0.98
    }
    ```
  *(Note: Currently returns a dummy response until the model is fully trained and integrated.)*
* **Error Response (400):**
    ```json
    {
        "error": "Invalid input: Missing 'text' key in JSON."
    }
    
Containerization: Docker

Deployment (Planned): AWS (e.g., Elastic Beanstalk), GitHub Actions for CI/CD

Project Structure