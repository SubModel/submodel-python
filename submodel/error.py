"""
runpd | error.py

This file contains the error classes for the submodel package.
"""

from typing import Optional


class SubModelError(Exception):
    """
    Base class for all submodel errors
    """

    def __init__(self, message: Optional[str] = None):
        super().__init__(message)
        self.message = message

    def __str__(self):
        if self.message:
            return self.message
        return super().__str__()


class AuthenticationError(SubModelError):
    """
    Raised when authentication fails
    """


class QueryError(SubModelError):
    """
    Raised when a API query fails
    """

    def __init__(self, message: Optional[str] = None, query: Optional[str] = None):
        super().__init__(message)
        self.query = query
