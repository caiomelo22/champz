import asyncio
import logging
import os
import smtplib
from email.message import EmailMessage
from urllib.parse import urlencode


logger = logging.getLogger(__name__)


def _as_bool(value: str) -> bool:
    return value.strip().lower() in {"1", "true", "yes", "on"}


def _send_smtp(message: EmailMessage) -> None:
    host = os.environ["SMTP_HOST"]
    port = int(os.getenv("SMTP_PORT", "587"))
    timeout = float(os.getenv("SMTP_TIMEOUT_SECONDS", "10"))
    username = os.getenv("SMTP_USERNAME")
    password = os.getenv("SMTP_PASSWORD")
    use_ssl = _as_bool(os.getenv("SMTP_USE_SSL", "false"))
    use_tls = _as_bool(os.getenv("SMTP_USE_TLS", "true"))

    smtp_class = smtplib.SMTP_SSL if use_ssl else smtplib.SMTP
    with smtp_class(host, port, timeout=timeout) as smtp:
        if use_tls and not use_ssl:
            smtp.starttls()
        if username:
            smtp.login(username, password or "")
        smtp.send_message(message)


async def send_verification_email(email: str, token: str) -> None:
    frontend_url = os.getenv("FRONTEND_URL", "http://localhost:8080").rstrip("/")
    verification_url = f"{frontend_url}/verify-email?{urlencode({'token': token})}"
    backend = os.getenv("EMAIL_BACKEND", "console").strip().lower()

    if backend == "console":
        logger.warning("Verification link for %s: %s", email, verification_url)
        return
    if backend != "smtp":
        raise RuntimeError("EMAIL_BACKEND must be either 'console' or 'smtp'.")

    sender = os.getenv("EMAIL_FROM")
    if not sender:
        raise RuntimeError("EMAIL_FROM is required when EMAIL_BACKEND=smtp.")

    message = EmailMessage()
    message["Subject"] = "Verify your Champz account"
    message["From"] = sender
    message["To"] = email
    message.set_content(
        "Verify your Champz account by opening this link:\n\n"
        f"{verification_url}\n\n"
        "If you did not create this account, you can ignore this message."
    )

    await asyncio.to_thread(_send_smtp, message)