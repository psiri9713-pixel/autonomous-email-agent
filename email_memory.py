import json
import os

MEMORY_FILE = "processed_emails.json"


def load_processed_emails():
    """Load previously processed email IDs."""

    if not os.path.exists(MEMORY_FILE):
        return []

    with open(MEMORY_FILE, "r") as file:
        return json.load(file)


def is_processed(email_id):
    """Check whether an email was already processed."""

    processed_emails = load_processed_emails()

    return email_id in processed_emails


def mark_as_processed(email_id):
    """Save an email ID as processed."""

    processed_emails = load_processed_emails()

    if email_id not in processed_emails:
        processed_emails.append(email_id)

    with open(MEMORY_FILE, "w") as file:
        json.dump(processed_emails, file, indent=4)


if __name__ == "__main__":

    test_id = "test_email_123"

    print("Already processed:", is_processed(test_id))

    mark_as_processed(test_id)

    print("After marking:", is_processed(test_id))