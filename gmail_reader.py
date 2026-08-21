from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
import os
import base64

SCOPES = ["https://www.googleapis.com/auth/gmail.readonly"]


def get_gmail_service():
    creds = None

    if os.path.exists("token.json"):
        creds = Credentials.from_authorized_user_file(
            "token.json",
            SCOPES
        )

    if not creds or not creds.valid:
        flow = InstalledAppFlow.from_client_secrets_file(
            "credentials.json",
            SCOPES
        )

        creds = flow.run_local_server(port=0)

        with open("token.json", "w") as token:
            token.write(creds.to_json())

    return build("gmail", "v1", credentials=creds)


def get_header(headers, name):

    for header in headers:
        if header["name"].lower() == name.lower():
            return header["value"]

    return ""


def get_body(payload):

    body = ""

    if "body" in payload and payload["body"].get("data"):
        body = payload["body"]["data"]

    elif "parts" in payload:

        for part in payload["parts"]:

            if part["mimeType"] == "text/plain":

                if part["body"].get("data"):
                    body = part["body"]["data"]
                    break

    if body:

        return base64.urlsafe_b64decode(body).decode(
            "utf-8",
            errors="ignore"
        )

    return ""


def read_emails():

    service = get_gmail_service()

    # Read ONLY unread emails
    results = service.users().messages().list(
        userId="me",
        labelIds=["INBOX", "UNREAD"],
        maxResults=20
    ).execute()

    messages = results.get("messages", [])

    print(f"\nFound {len(messages)} unread emails.\n")

    emails = []

    for message in messages:

        msg = service.users().messages().get(
            userId="me",
            id=message["id"],
            format="full"
        ).execute()

        headers = msg["payload"].get("headers", [])

        sender = get_header(headers, "From")
        subject = get_header(headers, "Subject")
        body = get_body(msg["payload"])

        email = {
            "id": message["id"],
            "sender": sender,
            "subject": subject,
            "body": body
        }

        emails.append(email)

        print("--------------------------------")
        print("From:", sender)
        print("Subject:", subject)
        print("Body:")
        print(body[:500])
        print("--------------------------------")

    return emails


if __name__ == "__main__":
    read_emails()