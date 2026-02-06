# --- Session-Daten für Auth ---
# --- path: /app/security/session_data.py ---

from typing import TypedDict

class SessionData(TypedDict):
    user_id: str
    issued_at: int
    roles: str
