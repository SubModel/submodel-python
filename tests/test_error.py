"""Unit tests for the error classes in the submodel.error module."""

import unittest

# Assuming the error classes are in a file named 'error.py'
from submodel.error import AuthenticationError, QueryError, SubModelError


class TestErrorClasses(unittest.TestCase):
    """Unit tests for the error classes in the submodel.error module."""

    def test_run_pod_error_with_message(self):
        """Test the SubModelError class with a message."""
        error_msg = "An error occurred"
        err = SubModelError(error_msg)
        self.assertEqual(str(err), error_msg)

    def test_run_pod_error_without_message(self):
        """Test the SubModelError class without a message."""
        err = SubModelError()
        self.assertEqual(str(err), "None")

    def test_authentication_error(self):
        """Test the AuthenticationError class."""
        error_msg = "Authentication failed"
        err = AuthenticationError(error_msg)
        self.assertEqual(str(err), error_msg)

    def test_query_error_with_message_and_query(self):
        """Test the QueryError class with a message and query."""
        error_msg = "Query failed"
        query_str = "SELECT * FROM some_table WHERE condition"
        err = QueryError(error_msg, query_str)
        self.assertEqual(str(err), error_msg)
        self.assertEqual(err.query, query_str)

    def test_query_error_without_message_and_query(self):
        """Test the QueryError class without a message or query."""
        err = QueryError()
        self.assertEqual(str(err), "None")
        self.assertIsNone(err.query)
