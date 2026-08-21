def get_emails():
    """
    Temporary email reader.
    Later this will connect to Gmail API.
    """

    emails = [
        {
            "id": 1,
            "sender": "hr@company.com",
            "subject": "Interview Invitation",
            "body": "You have been shortlisted for an interview."
        },
        {
            "id": 2,
            "sender": "team@company.com",
            "subject": "Urgent Meeting",
            "body": "Please join the meeting immediately."
        },
        {
            "id": 3,
            "sender": "shop@example.com",
            "subject": "Special Offer",
            "body": "Get 50% discount on selected products."
        }
    ]

    return emails


if __name__ == "__main__":
    emails = get_emails()

    for email in emails:
        print("\n--------------------")
        print("ID:", email["id"])
        print("From:", email["sender"])
        print("Subject:", email["subject"])
        print("Body:", email["body"])