from gmail_reader import read_emails
from email_classifier import classify_email
from email_generator import generate_reply
from email_memory import is_processed, mark_as_processed
from email_sender import send_email


MY_EMAIL = "psiri9713@gmail.com"


def run_agent():

    print("====================================")
    print("   AUTONOMOUS EMAIL AGENT")
    print("====================================")

    emails = read_emails()

    print("\nStarting autonomous processing...\n")

    for email in emails:

        print("====================================")
        print("From:", email["sender"])
        print("Subject:", email["subject"])

        # Check duplicate
        if is_processed(email["id"]):
            print("Status: Already processed")
            print("Action: SKIPPED")
            continue

        # Classify email
        category = classify_email(
            email["subject"],
            email["body"],
            email["sender"]
        )

        print("Category:", category)

        # Ignore unwanted emails
        if category == "Ignore":
            print("Action: IGNORED")
            mark_as_processed(email["id"])
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

        # Ask for approval
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
            else:
                print("Action: SEND FAILED")
                print("Email was NOT marked as processed.")

        else:

            print("Action: REPLY NOT SENT")
            print("Email was NOT marked as processed.")

        print("====================================")


if __name__ == "__main__":
    run_agent()