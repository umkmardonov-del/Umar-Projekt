# --- Passwort-Helper ---
#  --- path: app/security/passwords.py ----

from passlib.context import CryptContext
from passlib.exc import UnknownHashError, InvalidHashError

from typing import Final

PWD_CONTEXT: Final[CryptContext] = CryptContext(
    schemes=["argon2"],
    deprecated="auto",
    argon2__type="ID",
    argon2__memory_cost=65536,
    argon2__time_cost=4,
    argon2__parallelism=2,
)

def hash_password(password: str) -> str:
    if not isinstance(password, str):
        raise InvalidHashError("type(password) has to be a string.")

    hashed = PWD_CONTEXT.hash(password)

    return hashed


def verify_password(password: str, hashed: str) -> bool:
