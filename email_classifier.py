def classify_email(subject, body, sender=""):
    """
    Classifies emails using subject, body and sender.
    """

    subject_text = subject.lower()
    body_text = body.lower()
    sender_text = sender.lower()

    text = subject_text + " " + body_text + " " + sender_text

    # 1. Ignore own emails
    my_email = "psiri9713@gmail.com"

    if my_email.lower() in sender_text:
        return "Ignore"

    # 2. Security / system emails
    if any(word in text for word in [
        "security alert",
        "sign-in",
        "app password",
        "2-step verification",
        "two-step verification",
        "password was reset",
        "oauth application",
        "security event",
        "delivery status notification",
        "mailer-daemon",
        "delivery failure"
    ]):
        return "Ignore"

    # 3. Career emails
    if any(word in text for word in [
        "interview opportunity",
        "interview invitation",
        "job opportunity",
        "job opening",
        "career opportunity",
        "internship",
        "shortlisted"
    ]):
        return "Career"

    # 4. Meeting emails
    # Check subject first to avoid random body keyword matches.
    if any(word in subject_text for word in [
        "meeting",
        "appointment",
        "schedule",
        "call"
    ]):
        return "Meeting"

    # Check body only for strong meeting phrases.
    if any(phrase in body_text for phrase in [
        "schedule a meeting",
        "meeting request",
        "meeting confirmation",
        "meeting is confirmed",
        "confirm the meeting",
        "join the meeting"
    ]):
        return "Meeting"

    # 5. Finance
    if any(word in text for word in [
        "invoice",
        "payment",
        "bill",
        "receipt",
        "transaction"
    ]):
        return "Finance"

    # 6. Urgent
    if any(word in text for word in [
        "urgent",
        "asap",
        "immediately",
        "emergency"
    ]):
        return "Urgent"

    # 7. Promotional / newsletter
    if any(word in text for word in [
        "discount",
        "sale",
        "special offer",
        "premium",
        "promotion",
        "limited time",
        "subscribe",
        "unsubscribe",
        "exclusive offer",
        "get 12 months",
        "discover music",
        "exclusive access",
        "get more storage",
        "clean up space",
        "try new ai features"
    ]):
        return "Promotional"

    return "General"


if __name__ == "__main__":

    subject = "Interview opportunity"
    body = "We would like to invite you for an interview tomorrow."

    category = classify_email(
        subject,
        body,
        "hr@example.com"
    )

    print("Email Category:", category)