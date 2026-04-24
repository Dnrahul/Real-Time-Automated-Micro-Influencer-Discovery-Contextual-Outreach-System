"""
========================================
🤖 Automation Engine
========================================
Handles automated sending of outreach:
1. Email via SMTP (Gmail)
2. Instagram DM (mock/placeholder)

Currently runs in MOCK mode for safety.
Set USE_MOCK_DATA=false in .env for real sending.

Workflow:
1. Takes creators with generated outreach
2. Sends emails via SMTP (or logs in mock mode)
3. Sends Instagram DMs (mock — real requires Instagrapi)
4. Returns delivery status for each creator
"""

import sys, os, smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))
from config.settings import settings


def _send_email_smtp(to_email: str, subject: str, body: str) -> dict:
    """
    Send email via SMTP.
    In mock mode: logs instead of sending.
    In real mode: connects to SMTP server and sends.
    """
    if settings.USE_MOCK_DATA or not settings.SMTP_EMAIL:
        print(f"  [MOCK EMAIL] To: {to_email} | Subject: {subject[:50]}...")
        return {
            "status": "MOCK_SENT",
            "to": to_email,
            "timestamp": datetime.now().isoformat(),
            "message": "Email logged (mock mode — not actually sent)"
        }

    try:
        msg = MIMEMultipart()
        msg["From"] = f"{settings.SMTP_FROM_NAME} <{settings.SMTP_EMAIL}>"
        msg["To"] = to_email
        msg["Subject"] = subject
        msg.attach(MIMEText(body, "plain"))

        with smtplib.SMTP(settings.SMTP_HOST, settings.SMTP_PORT) as server:
            server.starttls()
            server.login(settings.SMTP_EMAIL, settings.SMTP_PASSWORD)
            server.send_message(msg)

        return {
            "status": "SENT",
            "to": to_email,
            "timestamp": datetime.now().isoformat(),
            "message": "Email sent successfully"
        }
    except Exception as e:
        return {
            "status": "FAILED",
            "to": to_email,
            "timestamp": datetime.now().isoformat(),
            "message": f"Error: {str(e)}"
        }


def _send_instagram_dm(username: str, message: str) -> dict:
    """
    Send Instagram DM.
    Always mock for now — real integration requires:
    - Instagrapi library (pip install instagrapi)
    - Or Apify Instagram DM Actor

    Pseudo-code for real implementation:
        from instagrapi import Client
        cl = Client()
        cl.login(INSTAGRAM_USERNAME, INSTAGRAM_PASSWORD)
        user_id = cl.user_id_from_username(username)
        cl.direct_send(message, [user_id])
    """
    print(f"  [MOCK DM] To: @{username} | Message: {message[:40]}...")
    return {
        "status": "MOCK_SENT",
        "to": f"@{username}",
        "timestamp": datetime.now().isoformat(),
        "message": "DM logged (mock mode — real requires Instagrapi)"
    }


def execute_outreach(creators: list) -> dict:
    """
    Execute automated outreach for all creators.

    Args:
        creators: List of creators with outreach messages

    Returns:
        Dictionary with delivery results and summary stats
    """
    results = []
    email_sent = 0
    dm_sent = 0
    failed = 0

    print(f"\n[Automation Engine] Executing outreach for {len(creators)} creators...")

    for creator in creators:
        outreach = creator.get("outreach", {})
        name = creator.get("name", "Unknown")
        delivery = {"name": name, "email_result": None, "dm_result": None}

        # Send Email
        email = creator.get("estimated_email", creator.get("email", ""))
        if email and outreach.get("email_body"):
            result = _send_email_smtp(
                to_email=email,
                subject=outreach["email_subject"],
                body=outreach["email_body"]
            )
            delivery["email_result"] = result
            if result["status"] in ("SENT", "MOCK_SENT"):
                email_sent += 1
            else:
                failed += 1

        # Send Instagram DM
        username = creator.get("username", creator.get("channel_handle", ""))
        if username and outreach.get("dm_message"):
            clean_username = username.replace("@", "")
            result = _send_instagram_dm(clean_username, outreach["dm_message"])
            delivery["dm_result"] = result
            if result["status"] in ("SENT", "MOCK_SENT"):
                dm_sent += 1
            else:
                failed += 1

        creator["delivery"] = delivery
        results.append(delivery)

    summary = {
        "total_creators": len(creators),
        "emails_sent": email_sent,
        "dms_sent": dm_sent,
        "failed": failed,
        "execution_time": datetime.now().isoformat()
    }

    print(f"\n[Automation Engine] Complete!")
    print(f"  Emails: {email_sent} sent")
    print(f"  DMs: {dm_sent} sent")
    print(f"  Failed: {failed}")

    return {"results": results, "summary": summary, "creators": creators}
