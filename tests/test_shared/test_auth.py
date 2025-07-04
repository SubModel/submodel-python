"""
Test shared functions related to authentication
"""

import importlib
import unittest
from unittest.mock import mock_open, patch


class TestAPIKey(unittest.TestCase):
    """Test the API key"""

    # The mocked TOML file
    CREDENTIALS = b"""
    [default]
    api_key = "SUBMODEL_API_KEY"
    """

    @patch("builtins.open", new_callable=mock_open, read_data=CREDENTIALS)
    def test_use_file_credentials(self, mock_file):
        """
        Test that the API key is read from the credentials file
        """
        import submodel  # pylint: disable=import-outside-toplevel

        importlib.reload(submodel)
        self.assertEqual(submodel.api_key, "SUBMODEL_API_KEY")
        assert mock_file.called
