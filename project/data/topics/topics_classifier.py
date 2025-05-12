import re

from apps.core.models import BillsTable

from .keywords import TOPIC_KEYWORDS


def get_topics_from_bill(bill: BillsTable) -> list[str]:
    """
    Determine relevant topics for a given bill based on keyword matches in its title and summary.

    Args:
        bill (BillsTable): A Django model instance representing a bill.

    Returns:
        list[str]: A list of topic names matched based on predefined keyword sets.
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
