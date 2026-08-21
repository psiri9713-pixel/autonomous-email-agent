import sqlite3

DATABASE_NAME = "email_agent.db"


def get_connection():
    return sqlite3.connect(DATABASE_NAME)


def initialize_database():
    conn = get_connection()
    cursor = conn.cursor()

    # Store incoming emails
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS emails (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            email_id TEXT UNIQUE,
            sender TEXT,
            subject TEXT,
            body TEXT
        )
    """)

    # Store AI classification and actions
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS actions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            email_id TEXT,
            intent TEXT,
            confidence REAL,
            action TEXT,
            reason TEXT,
            status TEXT
        )
    """)

    # Store follow-up/dispute tasks
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS tasks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            email_id TEXT,
            task_type TEXT,
            priority TEXT,
            status TEXT
        )
    """)

    conn.commit()
    conn.close()


def save_email(email):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT OR IGNORE INTO emails
        (email_id, sender, subject, body)
        VALUES (?, ?, ?, ?)
    """, (
        email["id"],
        email["sender"],
        email["subject"],
        email["body"]
    ))

    conn.commit()
    conn.close()


def save_action(
    email_id,
    intent,
    confidence,
    action,
    reason,
    status
):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO actions
        (email_id, intent, confidence, action, reason, status)
        VALUES (?, ?, ?, ?, ?, ?)
    """, (
        email_id,
        intent,
        confidence,
        action,
        reason,
        status
    ))

    conn.commit()
    conn.close()


def save_task(
    email_id,
    task_type,
    priority,
    status
):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO tasks
        (email_id, task_type, priority, status)
        VALUES (?, ?, ?, ?)
    """, (
        email_id,
        task_type,
        priority,
        status
    ))

    conn.commit()
    conn.close()