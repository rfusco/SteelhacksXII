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

def analyze_conversation(conversation: List[Sentence]) -> float:
    """
    Analyze sentiment for a whole conversation.
    Returns a length-weighted compound score between -1 and +1.
    """

    weighted_sum = 0.0
    total_weight = 0

    for s in conversation:
        scores = analyze_sentiment(s.text)
        weight = max(len(s.text.split()), 1)  # weight = word count
        weighted_sum += scores["compound"] * weight
        total_weight += weight

    return weighted_sum / total_weight


texts = [
    "I love spending time with my family.",
    "I went to the store to buy some bread.",
    "I feel unsafe and scared right now.",
    "I love the food, but the service is terrible.",
    "Im so so so so so sad and upset and sad!!!",
]
for t in texts:
    print(t)
    print(analyze_sentiment(t))

sentences = [Sentence(text=t, speaker="", sentiment={}) for t in texts]
batched = analyze_sentences(sentences)
print("\n\n\nBatched sentence sentiments:")
for s in batched:
    print(s.text, s.sentiment)

sentences = [Sentence(text=t, speaker="", sentiment={}) for t in texts]
# Compute overall conversation score
overall = analyze_conversation(sentences)
print("\n\n\nConversation sentiment (weighted avg):", overall)