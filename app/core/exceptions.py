# --- Custom Exceptions ---
# --- path: app/core/exceptions.py ---

class AppError(Exception):
    pass


class DomainError(AppError):
    pass


class InfraError(AppError):
    pass

# ------ InfraError Child-Klassen ------
class HashError(InfraError):
    pass


class JSONSerializationError(InfraError):
    pass


class JSONDeserializationError(InfraError):
    pass


# ------- DomainError Child-Klassen -------
class CorruptSessionError(DomainError):
    pass


class SessionTimeoutError(DomainError):
    pass


class NotPermittedError(DomainError):
    pass


class NotAuthorizedError(DomainError):
    pass