"""Exceptions raised by Swiftype Enterprise Client."""

class SwiftypeEnterpriseError(Exception):
    """Base class for all Swiftype Enterprise errors."""

class InvalidCredentials(SwiftypeEnterpriseError):
    """Raised when request cannot authenticate"""

class NonExistentRecord(SwiftypeEnterpriseError):
    """Raised when record does not exist"""

class RecordAlreadyExists(SwiftypeEnterpriseError):
    """Raised when record already exists"""

class BadRequest(SwiftypeEnterpriseError):
    """Raised when bad request"""

class Forbidden(SwiftypeEnterpriseError):
    """Raised when http forbidden"""
