import os
import resend


def send_newsletter(html: str) -> dict:
    resend.api_key = os.environ["RESEND_API_KEY"]
    sender = os.environ["SENDER_EMAIL"]
    recipients_raw = os.environ.get("RECIPIENTS", "")
    recipients = [r.strip() for r in recipients_raw.split(",") if r.strip()]

    if not recipients:
        raise ValueError("No recipients configured. Set the RECIPIENTS environment variable.")

    return resend.Emails.send({
        "from": sender,
        "to": recipients,
        "subject": "GitHub Trending Weekly — Tech Observatory",
        "html": html,
    })
