""" Tests for submodel.serverless.modules.sm_logger """

import os
import unittest
from unittest.mock import patch

from submodel.serverless.modules import sm_logger


class TestLogger(unittest.TestCase):
    """Tests for sm_logger"""

    def setUp(self) -> None:
        """
        Set up the logger for each test
        """
        self.logger = sm_logger.SubModelLogger()

    def test_default_log_level(self):
        """
        Tests that the default log level is DEBUG
        """
        defult_logger = sm_logger.SubModelLogger()

        self.assertEqual(defult_logger.level, "DEBUG")

    def test_singleton(self):
        """
        Tests that the logger is a singleton
        """
        logger1 = sm_logger.SubModelLogger()
        logger2 = sm_logger.SubModelLogger()

        self.assertIs(logger1, logger2)

    def test_set_log_level(self):
        """
        Tests that the log level can be set
        """
        logger = sm_logger.SubModelLogger()

        logger.set_level("TRACE")
        self.assertEqual(logger.level, "TRACE")

        logger.set_level("INFO")
        self.assertEqual(logger.level, "INFO")

        logger.set_level("WARN")
        self.assertEqual(logger.level, "WARN")

        logger.set_level(3)
        self.assertEqual(logger.level, "INFO")

    def test_call_log(self):
        """
        Tests that the logger can be called and logs the message to stdout if the log level is set.
        """
        log = sm_logger.SubModelLogger()

        with patch("submodel.serverless.modules.sm_logger.SubModelLogger.log") as mock_log:

            log.warn("Test log message")

            mock_log.assert_called_once_with("Test log message", "WARN", None)

        log.set_level(0)
        with patch(
            "submodel.serverless.modules.sm_logger.SubModelLogger.log"
        ) as mock_log, patch("builtins.print") as mock_print:

            log.debug("Test log message")

            mock_log.assert_called_once_with("Test log message", "DEBUG", None)
            mock_print.assert_not_called()

        # Reset log level
        log.set_level("DEBUG")

    def test_invalid_debug_level(self):
        """
        Tests that an invalid debug level raises an exception
        """
        logger = sm_logger.SubModelLogger()

        with self.assertRaises(ValueError):
            logger.set_level("INVALID")

        with self.assertRaises(ValueError):
            logger.set_level([])

    def test_debug_level_int(self):
        """
        Tests that the debug level can be set using an int
        """
        int_logger = sm_logger.SubModelLogger()

        with self.assertRaises(ValueError):
            int_logger.set_level(69)

    def test_log_secret(self):
        """
        Tests that the secret method censors secrets.
        Captures stdout and checks that the secret is censored.
        """
        with patch("submodel.serverless.modules.sm_logger.SubModelLogger.log") as mock_log:
            self.logger.secret("test_secret", "test_secret_value")
            mock_log.assert_called_once_with(
                "test_secret: t***************e", "INFO", None
            )

    def test_log_tip(self):
        """
        Tests that the tip method logs a tip.
        """
        with patch("submodel.serverless.modules.sm_logger.SubModelLogger.log") as mock_log:
            self.logger.tip("test_tip")
            mock_log.assert_called_once_with("test_tip", "TIP")

    def test_log_trace(self):
        """
        Tests that the trace method logs a trace.
        """
        with patch("submodel.serverless.modules.sm_logger.SubModelLogger.log") as mock_log:
            self.logger.trace("This is a trace message")
            mock_log.assert_called_once_with("This is a trace message", "TRACE", None)

            self.logger.trace("This is another trace message", "test-request-id")
            mock_log.assert_called_with(
                "This is another trace message", "TRACE", "test-request-id"
            )

    def test_log_job_id(self):
        """Tests that the log method logs a job id"""
        logger = sm_logger.SubModelLogger()
        job_id = "test_job_id"

        # Patch print to capture stdout
        with patch("builtins.print") as mock_print:
            logger.log("test_message", "INFO", job_id)

            mock_print.assert_called_once_with(
                "INFO   | test_job_id | test_message", flush=True
            )

            # Test with endpoint id set
            os.environ["SUBMODEL_ENDPOINT_ID"] = "test_endpoint_id"
            logger.log("test_message", "INFO", job_id)
            os.environ.pop("SUBMODEL_ENDPOINT_ID")

            mock_print.assert_called_with(
                '{"requestId": "test_job_id", "message": "test_message", "level": "INFO"}',
                flush=True,
            )

    def test_log_truncate(self):
        """Tests that the log method truncates"""
        logger = sm_logger.SubModelLogger()
        job_id = "test_job_id"
        long_message = "a" * (sm_logger.MAX_MESSAGE_LENGTH + 100)
        expected_start = "a" * (sm_logger.MAX_MESSAGE_LENGTH // 2)
        expected_end = "a" * (sm_logger.MAX_MESSAGE_LENGTH // 2)
        truncated_amount = len(long_message) - sm_logger.MAX_MESSAGE_LENGTH
        truncation_note = f"\n...TRUNCATED {truncated_amount} CHARACTERS...\n"
        truncated_message = expected_start + truncation_note + expected_end

        with patch("builtins.print") as mock_print:
            logger.log(long_message, "INFO", job_id)

            expected_log_output = f"INFO   | {job_id} | {truncated_message}"

            mock_print.assert_called_once_with(expected_log_output, flush=True)
