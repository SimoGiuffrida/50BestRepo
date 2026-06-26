import os
from unittest.mock import patch, MagicMock
from src.delivery import send_newsletter

def test_send_newsletter_calls_resend_with_all_recipients():
    html = "<html><body>Report</body></html>"

    with patch.dict(os.environ, {
        "RESEND_API_KEY": "re_test_key",
        "SENDER_EMAIL": "newsletter@test.com",
        "RECIPIENTS": "a@test.com,b@test.com",
    }):
        with patch("src.delivery.resend.Emails.send") as mock_send:
            mock_send.return_value = {"id": "abc123"}
            result = send_newsletter(html)

    mock_send.assert_called_once()
    call_args = mock_send.call_args[0][0]
    assert call_args["to"] == ["a@test.com", "b@test.com"]
    assert call_args["from"] == "newsletter@test.com"
    assert "<html>" in call_args["html"]

def test_send_newsletter_raises_if_recipients_missing():
    html = "<html><body>Report</body></html>"
    with patch.dict(os.environ, {
        "RESEND_API_KEY": "re_test",
        "SENDER_EMAIL": "s@test.com",
        "RECIPIENTS": "",
    }):
        try:
            send_newsletter(html)
            assert False, "Should have raised ValueError"
        except ValueError as e:
            assert "recipients" in str(e).lower()
