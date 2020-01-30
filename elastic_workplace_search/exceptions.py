"""Exceptions raised by Elastic Enterprise Search Client."""

class EnterpriseSearchError(Exception):
    """Base class for all Enterprise Search errors."""

class InvalidCredentials(EnterpriseSearchError):
    """Raised when request cannot authenticate"""

class NonExistentRecord(EnterpriseSearchError):
    """Raised when record does not exist"""

class RecordAlreadyExists(EnterpriseSearchError):
    """Raised when record already exists"""

class BadRequest(EnterpriseSearchError):
    """Raised when bad request"""

class Forbidden(EnterpriseSearchError):
    """Raised when http forbidden"""
