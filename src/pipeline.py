import pandas as pd
from classifier import classify_ticket
from responder import generate_response
from audit_logger import log_ticket


def run_pipeline(csv_path: str = "data/mock_tickets.csv"):
    df = pd.read_csv(csv_path)

    results = {
        "total": 0,
        "auto_resolved": 0,
        "escalated": 0,
        "by_category": {}
    }

    print("=" * 60)
    print("NORTHSTAR SUPPORT DEFLECTION MVP")
    print("Processing tickets...")
    print("=" * 60)

    for _, row in df.iterrows():
        ticket = {
            "ticket_id": row["ticket_id"],
            "customer_name": row["customer_name"],
            "message": row["message"]
        }

        classification = classify_ticket(ticket["message"])
        response = generate_response(ticket, classification)

        log_ticket(ticket, classification, response)

        results["total"] += 1
        category = classification["category"]

        if response["action"] == "AUTO_RESOLVED":
            results["auto_resolved"] += 1
        else:
            results["escalated"] += 1

        if category not in results["by_category"]:
            results["by_category"][category] = {
                "auto_resolved": 0,
                "escalated": 0
            }

        if response["action"] == "AUTO_RESOLVED":
            results["by_category"][category]["auto_resolved"] += 1
        else:
            results["by_category"][category]["escalated"] += 1

        status_icon = "✓" if response["action"] == "AUTO_RESOLVED" \
            else "↑"
        print(f"{status_icon} {ticket['ticket_id']} | "
              f"{category} | "
              f"Confidence: {classification['confidence']} | "
              f"{response['action']}")

    print("\n" + "=" * 60)
    print("PIPELINE COMPLETE — SUMMARY")
    print("=" * 60)
    print(f"Total tickets processed: {results['total']}")
    print(f"Auto-resolved: {results['auto_resolved']}")
    print(f"Escalated to human: {results['escalated']}")
    deflection_rate = (results['auto_resolved'] /
                       results['total'] * 100)
    print(f"Deflection rate: {deflection_rate:.1f}%")
    print("\nBy category:")

    for cat, counts in results["by_category"].items():
        print(f"  {cat}: "
              f"{counts['auto_resolved']} resolved, "
              f"{counts['escalated']} escalated")

    return results


if __name__ == "__main__":
    run_pipeline()