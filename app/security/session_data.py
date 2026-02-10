# --- Session-Daten für Auth ---
# --- path: /app/security/session_data.py ---

from typing import TypedDict


# --- SessionData als TypedDict ---
class SessionData(TypedDict):
    user_id: str
    issued_at: int
    permissions: list[str]


def is_session_data(store_data: SessionData) -> bool:
    if not isinstance(store_data["user_id"], str):
        return False

    if not type(store_data["issued_at"]) is int:
        return False

    if not isinstance(store_data["permissions"], list):
        return False

    return True
