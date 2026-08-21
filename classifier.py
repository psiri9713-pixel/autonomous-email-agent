import json
import os
from dotenv import load_dotenv

load_dotenv()

CONFIDENCE_THRESHOLD = 0.70


def classify_email(email_text):
    """
    Classifies an email into one of four supported intents.
    Returns intent, confidence, reason and recommended action.
    """

    text = email_text.lower()

    # Simple fallback classifier.
    # We will replace/enhance this with an LLM in the next step.

    if "congratulations" in text or "prize" in text or "winner" in text:
        return {
            "intent": "spam",
            "confidence": 0.99,
            "reason": "The email contains promotional or suspicious prize-related content.",
            "action": "mark_spam"
        }

    if "dispute" in text or "incorrect amount" in text or "wrong amount" in text:
        return {
            "intent": "dispute",
            "confidence": 0.90,
            "reason": "The email reports a problem or disagreement with an invoice.",
            "action": "create_dispute"
        }

    if "when will" in text and "invoice" in text:
        return {
            "intent": "payment_query",
            "confidence": 0.92,
            "reason": "The sender is asking about the payment status of an invoice.",
            "action": "create_followup"
        }

    if "invoice" in text and ("attached" in text or "submission" in text):
        return {
            "intent": "invoice_submission",
            "confidence": 0.96,
            "reason": "The email indicates that an invoice is being submitted.",
            "action": "log_invoice"
        }

    # Unknown/ambiguous email
    return {
        "intent": "unknown",
        "confidence": 0.50,
        "reason": "The email does not contain enough information to confidently determine its intent.",
        "action": "human_review"
    }


def requires_human_review(confidence):
    return confidence < CONFIDENCE_THRESHOLD