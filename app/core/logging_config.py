# --- Logging Setup ---
# --- path: /app/core/logging_config.py ---

from __future__ import annotations

import json
import logging
from datetime import datetime, timezone
from typing import Any

from app.core.settings import settings


class _JsonFormatter(logging.Formatter):
    def format(self, record: logging.LogRecord) -> str:
        payload: dict[str, Any] = {
            "ts": datetime.fromtimestamp(record.created, tz=timezone.utc).isoformat(),
            "level": record.levelname,
            "logger": record.name,
            "msg": record.getMessage(),
        }
        if record.exc_info:
            payload["exc_info"] = self.formatException(record.exc_info)
        return json.dumps(payload, ensure_ascii=False, separators=(",", ":"))


def configure_logging() -> None:
    """
    Minimal, app-eigene Logging-Konfiguration.

    Warum nötig:
    - Ohne Konfiguration ist das Root-Level standardmäßig WARNING.
      Deine `logger.info(...)` Aufrufe (z.B. im Lifespan) werden dann nicht angezeigt.
    - Uvicorn konfiguriert primär seine eigenen Logger; App-Logger sollten zuverlässig
      über das Root-Logging laufen.
    """

    level = getattr(logging, settings.LOG_LEVEL.upper(), logging.INFO)

    root = logging.getLogger()
    if not root.handlers:
        handler = logging.StreamHandler()
        if settings.LOG_JSON:
            handler.setFormatter(_JsonFormatter())
        else:
            handler.setFormatter(
                logging.Formatter("%(asctime)s %(levelname)s %(name)s: %(message)s")
            )
        root.addHandler(handler)

    root.setLevel(level)

    # Optional: Access-Logs abschalten (uvicorn.access)
    logging.getLogger("uvicorn.access").disabled = not settings.LOG_ACCESS

    if settings.LOG_SQL:
        logging.getLogger("sqlalchemy.engine").setLevel(logging.INFO)
