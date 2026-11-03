"""Log an allowlisted event, not raw request headers or document content."""
import json
from integration_core import audit_event


if __name__ == "__main__":
    event = audit_event(request_id="r-1", tool="search_notes", status="ok", duration_ms=12,
                        authorization="Bearer public-test-fixture", arguments={"secret": "never-log"},
                        document="private-text")
    text = json.dumps(event)
    assert "Bearer" not in text and "private-text" not in text and "never-log" not in text
    print(text)
