"""
sentiment.py
------------
Use NLTK's VADER sentiment analysis to score sentences.
"""
from nltk.sentiment import SentimentIntensityAnalyzer
from typing import Dict, List
from models import Sentence

# Initialize analyzer once
sia = SentimentIntensityAnalyzer()

def analyze_sentiment(text: str) -> Dict[str, float]:
    """
    Analyze sentiment of a sentence using VADER.
    :param text: Input text
    :return: dict with neg, neu, pos, and compound scores
    """
    if not text.strip():
        return {"neg": 0.0, "neu": 1.0, "pos": 0.0, "compound": 0.0}
    return sia.polarity_scores(text)

def analyze_sentences(sentences: List[Sentence]) -> List[Sentence]:
    """
    Update a list of Sentence objects with sentiment scores.
    Sentiment field will store the full dictionary.
    """
    for s in sentences:
        s.sentiment = analyze_sentiment(s.text)
    return sentences

sentences = [
    "I love spending time with my family.",
    "I went to the store to buy some bread.",
    "I feel unsafe and scared right now.",
    "I love the food, but the service is terrible.",
    "FUCK FUCK FUCK FUCK",
    "I just want to die already"
]
for s in sentences:
    print(s)
    print(analyze_sentiment(s))
    print()