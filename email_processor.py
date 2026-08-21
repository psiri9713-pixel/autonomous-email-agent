from email_reader import get_emails
from email_classifier import classify_email


def process_emails():
    emails = get_emails()

    for email in emails:
        category = classify_email(
            email["subject"],
            email["body"]
        )

        print("\n==============================")
        print("Email ID:", email["id"])
        print("From:", email["sender"])
        print("Subject:", email["subject"])
        print("Category:", category)
        print("==============================")


if __name__ == "__main__":
    process_emails()