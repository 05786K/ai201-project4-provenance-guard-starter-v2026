"""
The ops log — UNIT 9.

One JSON object per line in `logs/requests.jsonl`, one line per HTTP request,
whatever happened to it: a decision, a rejection (422 / 413 / 429), a 404, a
crash. It answers "what did the service do, and how long did it take" after the
fact.

It is deliberately separate from `audit.py`. The audit log is the record of
*decisions* and its shape is unchanged. This one is the record of *requests*.
The two link through `content_id`.

What came in is recorded as the text's length and a short hash, never the raw
text, so the log can be committed and shared without copying people's writing.

Logging must never break a request: `write` swallows its own errors.
"""

import hashlib
import json
import threading
import uuid
from datetime import datetime, timezone

import config

_lock = threading.Lock()

# Only these routes get their response body parsed for the log; /log and
# /health bodies are large or uninteresting.
_PARSED_ROUTES = ("/submit", "/appeal")


def new_request_id() -> str:
    return uuid.uuid4().hex[:12]


def _now() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="milliseconds")


def build_entry(request_id, request, response, duration_ms) -> dict:
    """Turn one finished request/response pair into a log record."""
    payload = request.get_json(silent=True)
    if not isinstance(payload, dict):
        payload = {}

    text = payload.get("text")
    creator_id = payload.get("creator_id")

    body = None
    if request.path in _PARSED_ROUTES:
        body = response.get_json(silent=True)
    if not isinstance(body, dict):
        body = {}

    status = response.status_code
    if status == 200 and "guess" in body:
        outcome = body["guess"]
    elif status == 200 and request.path == "/appeal":
        outcome = "appeal_recorded"
    elif status == 200:
        outcome = "ok"
    else:
        outcome = body.get("error") or f"http_{status}"

    return {
        "ts": _now(),
        "request_id": request_id,
        "method": request.method,
        "route": request.path,
        "status": status,
        "outcome": outcome,
        "duration_ms": round(duration_ms, 2),
        "creator_id": creator_id if isinstance(creator_id, str) else None,
        "text_len": len(text) if isinstance(text, str) else None,
        "text_sha8": (
            hashlib.sha256(text.encode("utf-8", "replace")).hexdigest()[:8]
            if isinstance(text, str) else None
        ),
        "content_id": body.get("content_id"),
        "model_score": body.get("model_score"),
        "style_score": body.get("style_score"),
        "combined_score": body.get("combined_score"),
    }


def write(entry: dict) -> None:
    """Append one record. Never raises."""
    try:
        config.OPS_LOG.parent.mkdir(parents=True, exist_ok=True)
        line = json.dumps(entry, ensure_ascii=False)
        with _lock:
            with config.OPS_LOG.open("a", encoding="utf-8") as f:
                f.write(line + "\n")
    except Exception:  # noqa: BLE001 — a logging failure must not fail the request
        pass
