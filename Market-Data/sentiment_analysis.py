import nltk
from nltk.sentiment import SentimentIntensityAnalyzer

nltk.download('vader_lexicon')
sia = SentimentIntensityAnalyzer()

def calculate_sentiment(text):
    sentiment = sia.polarity_scores(text)
    return sentiment['compound']