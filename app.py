import streamlit as st

from gmail_reader import read_emails
from email_classifier import classify_email
from email_generator import generate_reply
from email_memory import is_processed, mark_as_processed
from email_sender import send_email
from database import create_database, log_email, get_logs


# ==========================================
# PAGE CONFIGURATION
# ==========================================

st.set_page_config(
    page_title="Autonomous Email Agent",
    page_icon="📧",
    layout="wide"
)

create_database()


# ==========================================
# HEADER
# ==========================================

st.title("📧 Autonomous Email Agent")
st.caption("Intelligent Gmail automation and email management system")


# ==========================================
# SIDEBAR
# ==========================================

st.sidebar.header("Agent Controls")

scan_clicked = st.sidebar.button(
    "🔄 Scan Inbox"
)


# ==========================================
# LOAD EMAILS
# ==========================================

if scan_clicked:

    with st.spinner("Reading Gmail inbox..."):

        emails = read_emails()

    st.session_state["emails"] = emails

else:

    emails = st.session_state.get(
        "emails",
        []
    )


# ==========================================
# GET DATABASE LOGS
# ==========================================

logs = get_logs()


# ==========================================
# CALCULATE ACTIVITY METRICS
# ==========================================

sent_count = 0
rejected_count = 0
ignored_count = 0

for log in logs:

    action = log["action"]

    if action == "Sent":
        sent_count += 1

    elif action == "Rejected":
        rejected_count += 1

    elif action == "Ignored":
        ignored_count += 1


# ==========================================
# MAIN DASHBOARD
# ==========================================

if emails:

    categories = []

    for email in emails:

        category = classify_email(
            email["subject"],
            email["body"],
            email["sender"]
        )

        categories.append(category)


    total_emails = len(emails)

    ignored_current = categories.count(
        "Ignore"
    )

    actionable_emails = (
        total_emails - ignored_current
    )


    # ======================================
    # DASHBOARD METRICS
    # ======================================

    col1, col2, col3, col4, col5 = st.columns(5)

    with col1:

        st.metric(
            "📥 Total Emails",
            total_emails
        )

    with col2:

        st.metric(
            "🧠 Actionable",
            actionable_emails
        )

    with col3:

        st.metric(
            "🚫 Ignored",
            ignored_count
        )

    with col4:

        st.metric(
            "✅ Sent",
            sent_count
        )

    with col5:

        st.metric(
            "❌ Rejected",
            rejected_count
        )


    # ======================================
    # INBOX
    # ======================================

    st.divider()

    st.subheader("📨 Inbox")


    for email in emails:

        category = classify_email(
            email["subject"],
            email["body"],
            email["sender"]
        )


        with st.expander(
            f"{email['subject']} — {category}"
        ):

            st.write(
                f"**From:** {email['sender']}"
            )

            st.write(
                f"**Category:** {category}"
            )

            st.write("**Email Body:**")

            st.text(
                email["body"][:1500]
            )


            # ==================================
            # IGNORE EMAIL
            # ==================================

            if category == "Ignore":

                st.warning(
                    "This email will not receive an automatic reply."
                )

                continue


            # ==================================
            # ALREADY PROCESSED
            # ==================================

            if is_processed(
                email["id"]
            ):

                st.info(
                    "This email has already been processed."
                )

                continue


            # ==================================
            # GENERATE REPLY
            # ==================================

            reply = generate_reply(
                category,
                email["sender"],
                email["subject"],
                email["body"]
            )


            st.write(
                "**Generated Reply:**"
            )


            edited_reply = st.text_area(
                "Reply",
                value=reply,
                height=180,
                key=f"reply_{email['id']}"
            )


            col_send, col_reject = st.columns(2)


            # ==================================
            # SEND REPLY
            # ==================================

            with col_send:

                if st.button(
                    "✅ Send Reply",
                    key=f"send_{email['id']}"
                ):

                    with st.spinner(
                        "Sending reply..."
                    ):

                        success = send_email(
                            email["sender"],
                            "Re: " + email["subject"],
                            edited_reply
                        )


                    if success:

                        mark_as_processed(
                            email["id"]
                        )


                        log_email(
                            email["id"],
                            email["sender"],
                            email["subject"],
                            category,
                            edited_reply,
                            "Sent",
                            "Success"
                        )


                        st.success(
                            "Reply sent successfully!"
                        )

                    else:

                        log_email(
                            email["id"],
                            email["sender"],
                            email["subject"],
                            category,
                            edited_reply,
                            "Send",
                            "Failed"
                        )


                        st.error(
                            "Failed to send reply."
                        )


            # ==================================
            # REJECT REPLY
            # ==================================

            with col_reject:

                if st.button(
                    "❌ Reject",
                    key=f"reject_{email['id']}"
                ):

                    log_email(
                        email["id"],
                        email["sender"],
                        email["subject"],
                        category,
                        edited_reply,
                        "Rejected",
                        "Not Sent"
                    )


                    st.warning(
                        "Reply rejected. Email was not sent."
                    )


else:

    st.info(
        "Click 'Scan Inbox' from the sidebar to load your Gmail."
    )


# ==========================================
# CATEGORY ANALYTICS
# ==========================================

st.divider()

st.subheader(
    "📈 Email Category Analytics"
)


if emails:

    category_counts = {}


    for email in emails:

        category = classify_email(
            email["subject"],
            email["body"],
            email["sender"]
        )


        if category in category_counts:

            category_counts[category] += 1

        else:

            category_counts[category] = 1


    st.bar_chart(
        category_counts
    )

else:

    st.info(
        "Scan the inbox to view category analytics."
    )


# ==========================================
# ACTIVITY HISTORY
# ==========================================

st.divider()

st.subheader(
    "📊 Activity History"
)


logs = get_logs()


if logs:

    st.dataframe(
        logs,
        use_container_width=True,
        hide_index=True
    )

else:

    st.info(
        "No activity history available yet."
    )