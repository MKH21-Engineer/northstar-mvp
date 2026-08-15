from templates.order_status import ORDER_STATUS_TEMPLATES
from templates.returns import RETURNS_TEMPLATES


def select_template(category: str, message: str) -> str:
    message_lower = message.lower()

    if category == "order_status":
        if any(word in message_lower for word in
               ["late", "delayed", "no movement", "hasn't moved"]):
            return ORDER_STATUS_TEMPLATES["delayed"]
        elif any(word in message_lower for word in
                 ["can't find", "not found", "no order"]):
            return ORDER_STATUS_TEMPLATES["not_found"]
        else:
            return ORDER_STATUS_TEMPLATES["standard"]

    elif category == "returns_refunds":
        if any(word in message_lower for word in
               ["damaged", "broken", "arrived damaged", "wrong item"]):
            return RETURNS_TEMPLATES["damaged"]
        elif any(word in message_lower for word in
                 ["refund status", "where is my refund",
                  "still waiting", "when will i get"]):
            return RETURNS_TEMPLATES["refund_status"]
        else:
            return RETURNS_TEMPLATES["standard"]

    return None


def generate_response(ticket: dict,
                      classification: dict) -> dict:
    category = classification["category"]
    auto_resolve = classification["auto_resolve"]

    if not auto_resolve:
        return {
            "action": "ESCALATE",
            "response": None,
            "reason": f"Confidence {classification['confidence']}"
                      f" below threshold or stock query"
        }

    template = select_template(category, ticket["message"])

    if not template:
        return {
            "action": "ESCALATE",
            "response": None,
            "reason": "No template matched for this category"
        }

    response_text = template.format(
        customer_name=ticket["customer_name"],
        ticket_id=ticket["ticket_id"]
    )

    return {
        "action": "AUTO_RESOLVED",
        "response": response_text,
        "reason": f"Category: {category} | "
                  f"Confidence: {classification['confidence']}"
    }