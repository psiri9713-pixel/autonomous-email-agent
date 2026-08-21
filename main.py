from gmail_reader import read_emails
from email_classifier import classify_email
from email_generator import generate_reply
from email_memory import is_processed, mark_as_processed
from email_sender import send_email
from database import create_database, log_email


def run_agent():

    create_database()

    print("====================================")
    print("   AUTONOMOUS EMAIL AGENT")
    print("====================================")

    emails = read_emails()

    print("\nStarting autonomous processing...\n")

    for email in emails:

        print("====================================")
        print("From:", email["sender"])
        print("Subject:", email["subject"])

        # Duplicate check
        if is_processed(email["id"]):

            print("Status: Already processed")
            print("Action: SKIPPED")

            log_email(
                email["id"],
                email["sender"],
                email["subject"],
                "Already Processed",
                "",
                "Skipped",
                "Already Processed"
            )

            continue

        # Classification
        category = classify_email(
            email["subject"],
            email["body"],
            email["sender"]
        )

        print("Category:", category)

        # Ignore
        if category == "Ignore":

            print("Action: IGNORED")

            mark_as_processed(email["id"])

            log_email(
                email["id"],
                email["sender"],
                email["subject"],
                category,
                "",
                "Ignored",
                "Processed"
            )

            continue

        # Generate reply
        reply = generate_reply(
            category,
            email["sender"],
            email["subject"],
            email["body"]
        )

        print("\nGenerated Reply:")
        print("----------------")
        print(reply)

        # Approval
        print("\nDo you want to send this reply?")
        choice = input("Enter y/n: ").strip().lower()

        if choice == "y":

            success = send_email(
                email["sender"],
                "Re: " + email["subject"],
                reply
            )

            if success:

                print("Action: REPLY SENT")

                mark_as_processed(email["id"])

                log_email(
                    email["id"],
                    email["sender"],
                    email["subject"],
                    category,
                    reply,
                    "Sent",
                    "Success"
                )

            else:

                print("Action: SEND FAILED")

                log_email(
                    email["id"],
                    email["sender"],
                    email["subject"],
                    category,
                    reply,
                    "Send",
                    "Failed"
                )

        else:

            print("Action: REPLY NOT SENT")

            log_email(
                email["id"],
                email["sender"],
                email["subject"],
                category,
                reply,
                "Rejected",
                "Not Sent"
            )

        print("====================================")


if __name__ == "__main__":
    run_agent()