# --- Passwort-Helper ---
#  --- path: app/security/passwords.py ----

from logging import getLogger
from passlib.context import CryptContext
from passlib.exc import UnknownHashError, InvalidHashError
from secrets import token_urlsafe
from typing import Final

from app.core.exceptions import HashError


logger = getLogger(__name__)

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
        raise TypeError("'password' muss ein String sein.")

    hashed = PWD_CONTEXT.hash(password)

    return hashed


def verify_password(password: str, hashed: str) -> bool:
    if not isinstance(password, str) or not isinstance(hashed, str) or not hashed:
        raise TypeError("'password' und 'hashed' müssen Strings sein.")

    try:
         return PWD_CONTEXT.verify(password, hashed)

    except (UnknownHashError, InvalidHashError):
        logger.exception("Ein Fehler ist beim Verifizieren des PW-Hashed aufgetreten.")
        raise HashError()


def needs_rehash(hashed: str) -> bool:
    if not isinstance(hashed, str) or not hashed:
        raise TypeError("'hashed' muss ein String sein.")

    return PWD_CONTEXT.needs_update(hashed)

def generate_secret_token():
    token = token_urlsafe(32)
    return token
