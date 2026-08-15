import gspread
from google.oauth2.service_account import Credentials
from datetime import datetime, timezone
from pathlib import Path


SPREADSHEET_NAME = "Northstar MVP – Ticket Audit Log"

CREDENTIALS_FILE = (
    Path(__file__).resolve().parent.parent / "credentials.json"
)


def get_sheet():
    scopes = [
        "https://www.googleapis.com/auth/spreadsheets",
        "https://www.googleapis.com/auth/drive",
    ]

    creds = Credentials.from_service_account_file(
        CREDENTIALS_FILE,
        scopes=scopes,
    )

    gc = gspread.authorize(creds)

    spreadsheet = gc.open(SPREADSHEET_NAME)

    return spreadsheet.sheet1


def log_ticket(ticket: dict, classification: dict, response: dict):
    sheet = get_sheet()

    timestamp = datetime.now(timezone.utc).isoformat()

    row = [
        timestamp,
        ticket.get("id", ""),
        ticket.get("subject", ""),
        classification.get("category", ""),
        classification.get("priority", ""),
        response.get("status", ""),
        response.get("message", ""),
    ]

    sheet.append_row(
        row,
        value_input_option="USER_ENTERED",
    )

    print("✓ Ticket successfully written to Google Sheets")


if __name__ == "__main__":
    test_ticket = {
        "id": "TEST-001",
        "subject": "Test payment issue",
    }

    test_classification = {
        "category": "Payment",
        "priority": "High",
    }

    test_response = {
        "status": "Test",
        "message": "Google Sheets integration test successful.",
    }

    log_ticket(
        test_ticket,
        test_classification,
        test_response,
    )