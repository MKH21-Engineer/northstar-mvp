import os
from anthropic import Anthropic
from dotenv import load_dotenv

load_dotenv()

client = Anthropic()

ORDER_STATUS_KEYWORDS = [
    "where is my order", "has this shipped", "order status",
    "delivery", "track my order", "dispatched", "shipped yet",
    "when will it arrive", "shipping confirmation", "order number",
    "late", "package on the way", "when exactly"
]

RETURNS_KEYWORDS = [
    "return", "refund", "exchange", "damaged", "wrong size",
    "charged twice", "money back", "return policy", "return shipping",
    "get my refund", "refund process", "return this"
]

STOCK_KEYWORDS = [
    "back in stock", "available", "stock availability", "different size",
    "different color", "sold out", "restock", "restocking", "in stock",
    "carry this", "size available", "out of stock", "sku"
]


def keyword_classify(message: str) -> tuple[str, float]:
    message_lower = message.lower()

    scores = {
        "order_status": 0,
        "returns_refunds": 0,
        "stock_availability": 0
    }

    for keyword in ORDER_STATUS_KEYWORDS:
        if keyword in message_lower:
            scores["order_status"] += 1

    for keyword in RETURNS_KEYWORDS:
        if keyword in message_lower:
            scores["returns_refunds"] += 1

    for keyword in STOCK_KEYWORDS:
        if keyword in message_lower:
            scores["stock_availability"] += 1

    total_hits = sum(scores.values())

    if total_hits == 0:
        return "unknown", 0.0

    best_category = max(scores, key=scores.get)
    confidence = scores[best_category] / total_hits

    return best_category, round(confidence, 2)


def claude_classify(message: str) -> tuple[str, float]:
    response = client.messages.create(
        model="claude-sonnet-4-6",
        max_tokens=100,
        messages=[
            {
                "role": "user",
                "content": f"""Classify this customer support ticket into exactly one category.
                
Categories:
- order_status: questions about where an order is, shipping, delivery tracking
- returns_refunds: questions about returning items, getting refunds, exchanges
- stock_availability: questions about whether items are in stock, available sizes/colors

Ticket: "{message}"

Reply with ONLY this format:
CATEGORY: <category_name>
CONFIDENCE: <number between 0.0 and 1.0>"""
            }
        ]
    )

    response_text = response.content[0].text
    lines = response_text.strip().split("\n")

    category = "unknown"
    confidence = 0.5

    for line in lines:
        if line.startswith("CATEGORY:"):
            category = line.replace("CATEGORY:", "").strip()
        if line.startswith("CONFIDENCE:"):
            confidence = float(line.replace("CONFIDENCE:", "").strip())

    return category, confidence


def classify_ticket(message: str,
                    threshold: float = 0.85) -> dict:
    category, confidence = keyword_classify(message)

    method = "keyword"

    if confidence < threshold or category == "unknown":
        category, confidence = claude_classify(message)
        method = "claude_api"

    return {
        "category": category,
        "confidence": confidence,
        "method": method,
        "auto_resolve": confidence >= threshold and
                        category != "stock_availability"
    }