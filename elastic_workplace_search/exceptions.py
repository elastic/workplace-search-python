"""Exceptions raised by Elastic Workplace Search Client."""

class WorkplaceSearchError(Exception):
    """Base class for all Workplace Search errors."""

class InvalidCredentials(WorkplaceSearchError):
    """Raised when request cannot authenticate"""

class NonExistentRecord(WorkplaceSearchError):
    """Raised when record does not exist"""

class RecordAlreadyExists(WorkplaceSearchError):
    """Raised when record already exists"""

class BadRequest(WorkplaceSearchError):
    """Raised when bad request"""

class Forbidden(WorkplaceSearchError):
    """Raised when http forbidden"""
