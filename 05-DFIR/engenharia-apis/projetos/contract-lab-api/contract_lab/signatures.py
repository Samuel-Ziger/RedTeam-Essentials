"""Webhook signing helpers; they never send a network request."""

from __future__ import annotations

import hashlib
import hmac
import re
import time
from threading import RLock

EVENT_ID = re.compile(r"[A-Za-z0-9._:-]{1,128}")


def sign(body: bytes, secret: bytes, timestamp: int) -> str:
    if len(secret) < 16:
        raise ValueError("o segredo de laboratório deve ter ao menos 16 bytes")
    material = str(timestamp).encode() + b"." + body
    return "v1=" + hmac.new(secret, material, hashlib.sha256).hexdigest()


def verify(
    body: bytes,
    secret: bytes,
    timestamp: int,
    signature: str,
    *,
    now: int | None = None,
    tolerance_seconds: int = 300,
) -> bool:
    if isinstance(timestamp, bool) or not isinstance(timestamp, int):
        return False
    if not isinstance(signature, str) or len(signature) != 67:
        return False
    current = int(time.time()) if now is None else now
    if tolerance_seconds < 0 or abs(current - timestamp) > tolerance_seconds:
        return False
    expected = sign(body, secret, timestamp)
    return hmac.compare_digest(expected, signature)


class ReplayGuard:
    """Small in-memory replay guard for the local webhook laboratory."""

    def __init__(self) -> None:
        self._lock = RLock()
        self._seen: dict[str, int] = {}

    def accept(
        self,
        event_id: str,
        timestamp: int,
        *,
        now: int | None = None,
        tolerance_seconds: int = 300,
    ) -> bool:
        if not EVENT_ID.fullmatch(event_id):
            return False
        if isinstance(timestamp, bool) or not isinstance(timestamp, int):
            return False
        current = int(time.time()) if now is None else now
        if tolerance_seconds < 0 or abs(current - timestamp) > tolerance_seconds:
            return False
        cutoff = current - tolerance_seconds
        with self._lock:
            self._seen = {
                recorded_id: recorded_at for recorded_id, recorded_at in self._seen.items() if recorded_at >= cutoff
            }
            if event_id in self._seen:
                return False
            self._seen[event_id] = timestamp
            return True
