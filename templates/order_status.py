ORDER_STATUS_TEMPLATES = {
    "standard": """Hi {customer_name}, 

Thank you for reaching out to Northstar Retail Co.

You can track your order in real time using the link below:
Track My Order: https://northstar.co/track?ref={ticket_id}

If your order was placed within the last 24 hours,
tracking information may take up to 12 hours to activate.
Orders placed before 2PM on business days typically
ship same day.

If your tracking shows no movement for more than
3 business days, reply to this message and a team
member will investigate immediately.

Northstar Support Team""", 

    "delayed": """Hi {customer_name}, 

We can see your order is taking a little longer 
than expected and we sincerely apologize for 
the inconvenience. 

Your order is currently in transit. Our logistics
team has been notified. You should receive an
updated delivery window within 24 hours.

Track here: https://northstar.co/track?ref={ticket_id}

Thank you for your patience.

Northstar Support Team""",

    "not_found": """Hi {customer_name},

We were unable to locate an order with your details
automatically. This usually means the order was placed
under a different email address.

Please reply with your order number (found in your
confirmation email) and we will locate it for you
within 2 hours.

Northstar Support Team"""
}
