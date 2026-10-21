"""Application service: authorization, cursors, idempotency and use cases."""

from __future__ import annotations

import base64
import binascii
import hashlib
import hmac
import json
import re

from .domain import Event, Item, Principal, Status, normalize_title
from .errors import bad_request, forbidden
from .store import InMemoryStore

KEY = re.compile(r"[A-Za-z0-9._:-]{8,128}")
DEFAULT_CURSOR_SECRET = b"contract-lab-cursor-secret-v1"
MAX_CURSOR_LENGTH = 512


class ItemService:
    def __init__(
        self,
        store: InMemoryStore,
        *,
        cursor_secret: bytes = DEFAULT_CURSOR_SECRET,
    ) -> None:
        if len(cursor_secret) < 16:
            raise ValueError("cursor_secret deve possuir ao menos 16 bytes")
        self._store = store
        self._cursor_secret = cursor_secret

    def create(self, principal: Principal, title: str, idempotency_key: str) -> tuple[Item, bool]:
        self._require_writer(principal)
        if not KEY.fullmatch(idempotency_key):
            raise bad_request(
                "invalid-idempotency-key",
                "Idempotency-Key deve ter 8–128 caracteres seguros.",
            )
        normalized = normalize_title(title)
        fingerprint = hashlib.sha256(
            json.dumps({"title": normalized}, sort_keys=True, separators=(",", ":")).encode()
        ).hexdigest()
        return self._store.create(principal, normalized, idempotency_key, fingerprint)

    def get(self, principal: Principal, item_id: str) -> Item:
        return self._store.get(principal, item_id)

    def list_items(
        self,
        principal: Principal,
        *,
        after: str | None,
        limit: int,
        status: Status | None,
    ) -> tuple[list[Item], str | None]:
        if not 1 <= limit <= 100:
            raise bad_request("invalid-limit", "limit deve estar entre 1 e 100.")
        sequence = decode_cursor(after, status=status, secret=self._cursor_secret) if after is not None else 0
        matches = self._store.list_items(principal, sequence, limit + 1, status)
        page = matches[:limit]
        next_cursor = (
            encode_cursor(page[-1].sequence, status=status, secret=self._cursor_secret)
            if len(matches) > limit
            else None
        )
        return page, next_cursor

    def update(
        self,
        principal: Principal,
        item_id: str,
        expected_etag: str,
        *,
        title: str | None,
        status: Status | None,
    ) -> Item:
        self._require_writer(principal)
        if not expected_etag:
            raise bad_request("missing-if-match", "If-Match é obrigatório.")
        normalized = normalize_title(title) if title is not None else None
        return self._store.update(
            principal,
            item_id,
            expected_etag,
            title=normalized,
            status=status,
        )

    def events(self, principal: Principal, *, limit: int = 50) -> list[Event]:
        self._require_writer(principal)
        if not 1 <= limit <= 100:
            raise bad_request("invalid-limit", "limit deve estar entre 1 e 100.")
        return self._store.events(principal, limit=limit)

    @staticmethod
    def _require_writer(principal: Principal) -> None:
        if principal.role != "writer":
            raise forbidden()


def encode_cursor(
    sequence: int,
    *,
    status: Status | None = None,
    secret: bytes = DEFAULT_CURSOR_SECRET,
) -> str:
    if isinstance(sequence, bool) or not isinstance(sequence, int) or sequence < 0:
        raise ValueError("sequence deve ser um inteiro não negativo")
    document = {"v": 1, "sequence": sequence, "status": status}
    raw = json.dumps(document, sort_keys=True, separators=(",", ":")).encode()
    payload = base64.urlsafe_b64encode(raw).decode().rstrip("=")
    signature = hmac.new(secret, payload.encode(), hashlib.sha256).hexdigest()
    return f"{payload}.{signature}"


def decode_cursor(
    value: str,
    *,
    status: Status | None = None,
    secret: bytes = DEFAULT_CURSOR_SECRET,
) -> int:
    try:
        if not 1 <= len(value) <= MAX_CURSOR_LENGTH:
            raise ValueError
        payload, supplied_signature = value.split(".", maxsplit=1)
        if len(supplied_signature) != 64:
            raise ValueError
        expected_signature = hmac.new(secret, payload.encode(), hashlib.sha256).hexdigest()
        if not hmac.compare_digest(expected_signature, supplied_signature):
            raise ValueError
        padding = "=" * (-len(payload) % 4)
        raw = base64.b64decode(payload + padding, altchars=b"-_", validate=True)
        document = json.loads(raw)
        if set(document) != {"v", "sequence", "status"} or document["v"] != 1:
            raise ValueError
        sequence = document["sequence"]
        if isinstance(sequence, bool) or not isinstance(sequence, int) or sequence < 0:
            raise ValueError
        if document["status"] != status:
            raise ValueError
        return sequence
    except (
        ValueError,
        TypeError,
        json.JSONDecodeError,
        UnicodeDecodeError,
        binascii.Error,
    ) as exc:
        raise bad_request("invalid-cursor", "O cursor é inválido.") from exc
