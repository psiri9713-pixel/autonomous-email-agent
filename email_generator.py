def generate_reply(category, sender, subject, body):
    """
    Generates an automatic reply based on email category
    and the actual email content.
    """

    if category == "Ignore":
        return None

    if category == "Urgent":
        reply = (
            f"Hello,\n\n"
            f"I received your email regarding '{subject}'. "
            f"I understand that this matter is urgent and I will "
            f"look into it as soon as possible.\n\n"
            f"Regards,\n"
            f"Autonomous Email Agent"
        )

    elif category == "Meeting":
        reply = (
            f"Hello,\n\n"
            f"Thank you for contacting me regarding '{subject}'. "
            f"I have received the meeting details and will review "
            f"the schedule shortly.\n\n"
            f"Regards,\n"
            f"Autonomous Email Agent"
        )

    elif category == "Finance":
        reply = (
            f"Hello,\n\n"
            f"Thank you for sending the financial information regarding "
            f"'{subject}'. I have received the details and will review "
            f"them carefully.\n\n"
            f"Regards,\n"
            f"Autonomous Email Agent"
        )

    elif category == "Career":
        reply = (
            f"Hello,\n\n"
            f"Thank you for contacting me regarding '{subject}'. "
            f"I appreciate the opportunity and will review the "
            f"information provided.\n\n"
            f"Regards,\n"
            f"Autonomous Email Agent"
        )

    elif category == "Promotional":
        reply = (
            f"Hello,\n\n"
            f"Thank you for sharing the information regarding "
            f"'{subject}'. I have received your message.\n\n"
            f"Regards,\n"
            f"Autonomous Email Agent"
        )

    else:
        reply = (
            f"Hello,\n\n"
            f"Thank you for your email regarding '{subject}'. "
            f"I have received your message and will respond soon.\n\n"
            f"Regards,\n"
            f"Autonomous Email Agent"
        )

    return reply


if __name__ == "__main__":

    category = "Career"
    sender = "hr@company.com"
    subject = "Interview Invitation"
    body = "You have been shortlisted for an interview."

    reply = generate_reply(
        category,
        sender,
        subject,
        body
    )

    print("Generated Reply:")
    print("----------------")
    print(reply)