import re

from .keywords import TOPIC_KEYWORDS


def get_topics_from_bill(bill) -> list:
    """
    Accepts a Django Bill model instance and returns relevant topics based on its title and summary.
    """
    title = bill.title or ""
    summary = bill.summary or ""
    text = f"{title} {summary}".lower()
    words = set(re.findall(r"\b\w+\b", text))

    matched_topics = []
    for topic, keywords in TOPIC_KEYWORDS.items():
        if any(keyword in words for keyword in keywords):
            matched_topics.append(topic)

    return matched_topics
