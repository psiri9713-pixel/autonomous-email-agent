import sqlite3
from datetime import datetime

DB_NAME = "email_agent.db"


def create_database():
    connection = sqlite3.connect(DB_NAME)
    cursor = connection.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS email_logs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            email_id TEXT UNIQUE,
            sender TEXT,
            subject TEXT,
            category TEXT,
            reply TEXT,
            action TEXT,
            status TEXT,
            processed_at TEXT
        )
    """)

    connection.commit()
    connection.close()


def log_email(
    email_id,
    sender,
    subject,
    category,
    reply,
    action,
    status
):
    connection = sqlite3.connect(DB_NAME)
    cursor = connection.cursor()

    try:
        cursor.execute("""
            INSERT INTO email_logs (
                email_id,
                sender,
                subject,
                category,
                reply,
                action,
                status,
                processed_at
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            email_id,
            sender,
            subject,
            category,
            reply,
            action,
            status,
            datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        ))

        connection.commit()

    except sqlite3.IntegrityError:
        pass

    connection.close()


def get_logs():
    connection = sqlite3.connect(DB_NAME)
    cursor = connection.cursor()

    cursor.execute("""
        SELECT
            sender,
            subject,
            category,
            action,
            status,
            processed_at
        FROM email_logs
        ORDER BY id DESC
    """)

    rows = cursor.fetchall()
    connection.close()

    columns = [
        "sender",
        "subject",
        "category",
        "action",
        "status",
        "processed_at"
    ]

    logs = []

    for row in rows:
        logs.append(dict(zip(columns, row)))

    return logs


if __name__ == "__main__":
    create_database()
    print("Database created successfully.")