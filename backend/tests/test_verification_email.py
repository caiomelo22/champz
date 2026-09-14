import logging

import pytest

from app.auth import email as email_service


async def test_console_email_logs_encoded_verification_link(monkeypatch, caplog):
    monkeypatch.setenv("EMAIL_BACKEND", "console")
    monkeypatch.setenv("FRONTEND_URL", "https://champz.example/")

    with caplog.at_level(logging.WARNING):
        await email_service.send_verification_email("person@example.com", "token with spaces")

    assert "person@example.com" in caplog.text
    assert "https://champz.example/verify-email?token=token+with+spaces" in caplog.text


async def test_smtp_email_uses_configured_sender(monkeypatch):
    delivered = []

    async def capture_thread_call(function, message):
        delivered.append((function, message))

    monkeypatch.setenv("EMAIL_BACKEND", "smtp")
    monkeypatch.setenv("EMAIL_FROM", "Champz <no-reply@champz.example>")
    monkeypatch.setenv("FRONTEND_URL", "https://champz.example")
    monkeypatch.setattr(email_service.asyncio, "to_thread", capture_thread_call)

    await email_service.send_verification_email("person@example.com", "verification-token")

    assert len(delivered) == 1
    function, message = delivered[0]
    assert function is email_service._send_smtp
    assert message["From"] == "Champz <no-reply@champz.example>"
    assert message["To"] == "person@example.com"
    assert "https://champz.example/verify-email?token=verification-token" in message.get_content()


async def test_unknown_email_backend_is_rejected(monkeypatch):
    monkeypatch.setenv("EMAIL_BACKEND", "unknown")

    with pytest.raises(RuntimeError, match="console.*smtp"):
        await email_service.send_verification_email("person@example.com", "token")