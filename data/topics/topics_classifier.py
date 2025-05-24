import re

from .keywords import TOPIC_KEYWORDS
from .stopwords import STOPWORDS


def get_topics_from_bill(bill_title: str, bill_summary: str) -> list[str]:
    """
    Determine relevant topics for a given bill based on keyword matches in its title and summary.

    Args:
        bill (BillsTable): A Django model instance representing a bill.

    Returns:
        list[str]: A list of topic names matched based on predefined keyword sets.
    """
    combined_text = f"{bill_title} {bill_summary}"
    cleaned_text = re.sub(r"[^a-zA-Z\s]", "", combined_text).lower()
    tokens = [word for word in cleaned_text.split() if word not in STOPWORDS]

    unigrams = set(tokens)
    bigrams = {f"{tokens[i]} {tokens[i + 1]}" for i in range(len(tokens) - 1)}
    all_tokens = unigrams | bigrams

    matched_topics = []
    for topic, keywords in TOPIC_KEYWORDS.items():
        if all_tokens & keywords:
            matched_topics.append(topic)

    return matched_topics
