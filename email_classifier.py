def classify_email(subject, body, sender=""):
    text = (subject + " " + body).lower()
    my_email = "psiri9713@gmail.com"

    if my_email.lower() in sender.lower():
        return "Ignore"
    """
    Classifies an email based on its subject and body.
    """

    text = (subject + " " + body).lower()

    # Emails that should NOT receive automatic replies
    if any(word in text for word in [
        "security alert",
        "sign-in",
        "app password",
        "2-step verification",
        "two-step verification",
        "delivery status notification",
        "mailer-daemon",
        "delivery failure"
    ]):
        return "Ignore"

    elif any(word in text for word in [
        "urgent",
        "asap",
        "immediately",
        "emergency"
    ]):
        return "Urgent"

    elif any(word in text for word in [
        "meeting",
        "schedule",
        "appointment",
        "call"
    ]):
        return "Meeting"

    elif any(word in text for word in [
        "invoice",
        "payment",
        "bill",
        "receipt"
    ]):
        return "Finance"

    elif any(word in text for word in [
        "job",
        "interview",
        "career",
        "internship"
    ]):
        return "Career"

    elif any(word in text for word in [
        "offer",
        "discount",
        "sale",
        "promotion"
    ]):
        return "Promotional"

    else:
        return "General"


if __name__ == "__main__":

    subject = "Urgent meeting tomorrow"
    body = "Please join the meeting immediately."

    category = classify_email(subject, body)

    print("Email Category:", category)