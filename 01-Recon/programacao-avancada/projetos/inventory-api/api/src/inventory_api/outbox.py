"""Background projector from the PostgreSQL outbox to MongoDB."""

from __future__ import annotations

import logging
import threading
from datetime import datetime, timezone
from typing import Any

LOGGER = logging.getLogger(__name__)


class OutboxWorker:
    def __init__(self, source: Any, destination: Any, interval_seconds: float) -> None:
        self.source = source
        self.destination = destination
        self.interval_seconds = interval_seconds
        self._stop = threading.Event()
        self._thread = threading.Thread(target=self._run, name="outbox-worker", daemon=True)

    def start(self) -> None:
        self._thread.start()

    def stop(self, timeout: float = 5) -> None:
        self._stop.set()
        self._thread.join(timeout=timeout)
        if self._thread.is_alive():
            LOGGER.warning("outbox_worker_stop_timeout")

    def _run(self) -> None:
        while not self._stop.is_set():
            try:
                processed = self.run_once()
            except Exception:  # noqa: BLE001 - worker must retry after transient dependencies
                LOGGER.exception("outbox_iteration_failed")
                processed = 0
            if processed == 0:
                self._stop.wait(self.interval_seconds)

    def run_once(self) -> int:
        events = self.source.pending_events()
        processed = 0
        for event in events:
            if self._stop.is_set():
                break
            self.destination.publish(event)
            self.source.mark_published(event["id"], datetime.now(timezone.utc))
            processed += 1
        return processed
