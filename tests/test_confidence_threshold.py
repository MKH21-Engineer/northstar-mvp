from src.responder import generate_response

def test_below_85_percent_escalates():
    """
    A ticket with confidence below 85% must not be auto-resolved.
    """

    classification = {
        "category": "order_status",
        "confidence": 0.84,
        "method": "test",
        "auto_resolve": 0.84 >= 0.85
    }

    ticket = {
        "ticket_id": "TEST-084",
        "customer_name": "Test Customer",
        "message": "Where is my order?"
    }

    response = generate_response(ticket, classification)

    assert classification["auto_resolve"] is False
    assert response["action"] == "ESCALATE"


def test_exactly_85_percent_is_allowed():
    """
    Exactly 85% is not below the threshold.
    Therefore it should be eligible for auto-resolution
    when the category has a response template.
    """

    classification = {
        "category": "order_status",
        "confidence": 0.85,
        "method": "test",
        "auto_resolve": 0.85 >= 0.85
    }

    ticket = {
        "ticket_id": "TEST-085",
        "customer_name": "Test Customer",
        "message": "Where is my order?"
    }

    response = generate_response(ticket, classification)

    assert classification["auto_resolve"] is True
    assert response["action"] == "AUTO_RESOLVED"


def test_above_85_percent_is_allowed():
    """
    Confidence above 85% should be eligible for auto-resolution.
    """

    classification = {
        "category": "order_status",
        "confidence": 0.90,
        "method": "test",
        "auto_resolve": 0.90 >= 0.85
    }

    ticket = {
        "ticket_id": "TEST-090",
        "customer_name": "Test Customer",
        "message": "Where is my order?"
    }

    response = generate_response(ticket, classification)

    assert classification["auto_resolve"] is True
    assert response["action"] == "AUTO_RESOLVED"


def test_stock_availability_escalates():
    """
    Stock availability should escalate even with high confidence,
    because the existing classifier excludes stock_availability
    from auto-resolution.
    """

    classification = {
        "category": "stock_availability",
        "confidence": 0.95,
        "method": "test",
        "auto_resolve": 0.95 >= 0.85 and
                        "stock_availability" != "stock_availability"
    }

    ticket = {
        "ticket_id": "TEST-STOCK",
        "customer_name": "Test Customer",
        "message": "Is this item back in stock?"
    }

    response = generate_response(ticket, classification)

    assert classification["auto_resolve"] is False
    assert response["action"] == "ESCALATE"