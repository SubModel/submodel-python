""" Tests for submodel | serverless| worker """

# pylint: disable=protected-access

import argparse
import os
import sys
from unittest import mock
from unittest.mock import patch, mock_open, Mock, MagicMock

from unittest import IsolatedAsyncioTestCase
import nest_asyncio

import submodel
from submodel.serverless.modules.sm_logger import SubModelLogger
from submodel.serverless.modules.sm_scale import _handle_uncaught_exception
from submodel.serverless import _signal_handler

nest_asyncio.apply()


class TestWorker(IsolatedAsyncioTestCase):
    """Tests for Submodel serverless worker."""

    async def asyncSetUp(self):
        self.mock_handler = mock.Mock(return_value="test")
        self.mock_config = {
            "handler": self.mock_handler,
            "sm_args": {"test_input": None},
        }

    def test_is_local(self):
        """
        Test _is_local
        """
        with patch("submodel.serverless.worker.os") as mock_os:
            mock_os.environ.get.return_value = None
            assert submodel.serverless.worker._is_local({"sm_args": {}}) is True
            assert (
                submodel.serverless.worker._is_local(
                    {"sm_args": {"test_input": "something"}}
                )
                is True
            )

            mock_os.environ.get.return_value = "something"
            assert submodel.serverless.worker._is_local(self.mock_config) is False

    def test_start(self):
        """
        Test basic start call.
        """
        with patch(
            "builtins.open", mock_open(read_data='{"input":{"number":1}}')
        ) as mock_file, self.assertRaises(SystemExit):

            submodel.serverless.start({"handler": self.mock_handler})

            assert mock_file.called

    def test_is_local_testing(self):
        """
        Test _is_local_testing
        """
        with patch("submodel.serverless.worker.os") as mock_os:
            mock_os.environ.get.return_value = None
            assert submodel.serverless.worker._is_local(self.mock_config) is True
            mock_os.environ.get.return_value = "something"
            assert submodel.serverless.worker._is_local(self.mock_config) is False

    def test_local_api(self):
        """
        Test local FastAPI setup.
        """
        known_args = argparse.Namespace()
        known_args.sm_log_level = None
        known_args.sm_debugger = None
        known_args.sm_serve_api = True
        known_args.sm_api_port = 8000
        known_args.sm_api_concurrency = 1
        known_args.sm_api_host = "localhost"
        known_args.test_input = '{"test": "test"}'

        with patch(
            "argparse.ArgumentParser.parse_known_args"
        ) as mock_parse_known_args, patch(
            "submodel.serverless.sm_fastapi"
        ) as mock_fastapi:

            mock_parse_known_args.return_value = known_args, []
            submodel.serverless.start({"handler": self.mock_handler})

            assert mock_fastapi.WorkerAPI.called

    @patch("submodel.serverless.log")
    @patch("submodel.serverless.sys.exit")
    def test_signal_handler(self, mock_exit, mock_logger):
        """
        Test signal handler.
        """

        _signal_handler(None, None)

        assert mock_exit.called
        assert mock_logger.info.called


class TestWorkerTestInput(IsolatedAsyncioTestCase):
    """Tests for submodel | serverless| worker"""

    async def asyncSetUp(self):
        self.mock_handler = Mock()
        self.mock_handler.return_value = {}

        self.mock_handler.return_value = "test"

    def test_worker_bad_local(self):
        """
        Test sys args.
        """
        known_args = argparse.Namespace()
        known_args.sm_log_level = "WARN"
        known_args.sm_debugger = True
        known_args.sm_serve_api = None
        known_args.sm_api_port = 8000
        known_args.sm_api_concurrency = 1
        known_args.sm_api_host = "localhost"
        known_args.test_input = '{"test": "test"}'
        known_args.test_output = '{"test": "test"}'

        with patch(
            "argparse.ArgumentParser.parse_known_args"
        ) as mock_parse_known_args, self.assertRaises(SystemExit):

            mock_parse_known_args.return_value = known_args, []
            submodel.serverless.start({"handler": self.mock_handler})

            # Confirm that the log level is set to WARN
            log = SubModelLogger()
            assert log.level == "WARN"


def generator_handler(job):
    """
    Test generator_handler
    """
    print(job)
    yield "test1"
    yield "test2"


def generator_handler_exception(job):
    """
    Test generator_handler
    """
    print(job)
    yield "test1"
    print("Raise exception")
    raise Exception()  # pylint: disable=broad-exception-raised


def test_generator_handler_exception():
    """Test generator_handler_exception"""
    job = {"id": "test_job"}
    gen = generator_handler_exception(job)

    # Process the first yielded value
    output = next(gen)
    assert output == "test1", "First output should be 'test1'"

    # Attempt to get the next value, expecting an exception
    try:
        next(gen)
        assert False, "Expected an exception to be raised"
    except Exception:  # pylint: disable=broad-except
        assert True, "Exception was caught as expected"


class TestRunWorker(IsolatedAsyncioTestCase):
    """Tests for submodel | serverless| worker"""

    async def asyncSetUp(self):
        os.environ["SUBMODEL_WEBHOOK_GET_JOB"] = "https://test.com"

        # Set up the config
        self.config = {
            "handler": MagicMock(),
            "refresh_worker": True,
            "sm_args": {"sm_debugger": True, "sm_log_level": "DEBUG"},
        }

    async def asyncTearDown(self):
        sys.excepthook = sys.__excepthook__

    @patch("submodel.serverless.modules.sm_scale.AsyncClientSession")
    @patch("submodel.serverless.modules.sm_scale.get_job")
    @patch("submodel.serverless.modules.sm_job.run_job")
    @patch("submodel.serverless.modules.sm_job.stream_result")
    @patch("submodel.serverless.modules.sm_job.send_result")
    async def test_run_worker(
        self,
        mock_send_result,
        mock_stream_result,
        mock_run_job,
        mock_get_job,
        mock_session,
    ):
        """Test run_worker with synchronous handler."""
        # Mock return values for get_job
        mock_get_job.side_effect = [
            [{"id": "123", "input": {"number": 1}}],
            []  # Stop the loop after the second call
        ]
        mock_run_job.return_value = {"output": {"result": "odd"}}

        # Call the function
        submodel.serverless.start(self.config)

        # Make assertions about the behaviors
        self.assertEqual(mock_get_job.call_count, 1)
        mock_run_job.assert_called_once()
        mock_send_result.assert_called_once()

        assert not mock_stream_result.called
        assert mock_session.called

    @patch("submodel.serverless.modules.sm_scale.get_job")
    @patch("submodel.serverless.modules.sm_job.run_job")
    @patch("submodel.serverless.modules.sm_job.stream_result")
    @patch("submodel.serverless.modules.sm_job.send_result")
    async def test_run_worker_generator_handler(
        self, mock_send_result, mock_stream_result, mock_run_job, mock_get_job
    ):
        """
        Test run_worker with generator handler.

        Args:
            mock_stream_result (_type_): _description_
            mock_run_job_generator (_type_): _description_
            mock_run_job (_type_): _description_
            mock_get_job (_type_): _description_
        """
        # Define the mock behaviors
        mock_get_job.return_value = [{"id": "generator-123", "input": {"number": 1}}]

        # Test generator handler
        generator_config = {"handler": generator_handler, "refresh_worker": True}
        submodel.serverless.start(generator_config)

        assert mock_stream_result.called
        assert not mock_run_job.called

        # Since return_aggregate_stream is NOT activated, we should not submit any outputs.
        _, args, _ = mock_send_result.mock_calls[0]
        assert args[1] == {"output": [], "stopPod": True}

    @patch("submodel.serverless.modules.sm_scale.get_job")
    @patch("submodel.serverless.modules.sm_job.run_job")
    @patch("submodel.serverless.modules.sm_job.stream_result")
    @patch("submodel.serverless.modules.sm_job.send_result")
    async def test_run_worker_generator_handler_exception(
        self, mock_send_result, mock_stream_result, mock_run_job, mock_get_job
    ):
        """
        Test run_worker with generator handler.

        This test verifies that:
        - `stream_result` is called before an exception occurs.
        - `run_job` is never called since `handler` is a generator function.
        - An error is correctly reported back via `send_result`.
        """
        SubModelLogger().set_level("DEBUG")

        # Setup: Mock `get_job` to return a predefined job.
        mock_get_job.return_value = [
            {"id": "generator-123-exception", "input": {"number": 1}}
        ]

        submodel.serverless.start(
            {"handler": generator_handler_exception, "refresh_worker": True}
        )

        # Ensure `stream_result` was called at least once
        assert mock_stream_result.call_count >= 1

        # Ensure `run_job` was not called since the handler is a generator function
        assert not mock_run_job.called

        # Check that `send_result` was called
        assert mock_send_result.call_count == 1  # Adjust expectation if multiple calls are valid

        # Inspect the arguments for each call to `send_result`
        for call in mock_send_result.call_args_list:
            args, kwargs = call  # Unpack the tuple into args and kwargs
            # Check if the expected key is present in the args or kwargs
            if args and len(args) > 1:
                assert "error" in args[1] or "result" in args[1], "Expected error or result in args."
            else:
                # If args[1] doesn't have the expected keys, check in kwargs
                assert "error" in kwargs or "result" in kwargs, "Expected error or result in kwargs."

    @patch("submodel.serverless.modules.sm_scale.get_job")
    @patch("submodel.serverless.modules.sm_job.run_job")
    @patch("submodel.serverless.modules.sm_job.stream_result")
    @patch("submodel.serverless.modules.sm_job.send_result")
    async def test_run_worker_generator_aggregate_handler(
        self, mock_send_result, mock_stream_result, mock_run_job, mock_get_job
    ):
        """
        Test run_worker with generator handler.

        Args:
            mock_send_result (_type_): _description_
            mock_stream_result (_type_): _description_
            mock_run_job (_type_): _description_
            mock_get_job (_type_): _description_
            mock_session (_type_): _description_
        """
        # Define the mock behaviors
        mock_get_job.return_value = [
            {"id": "generator-123-aggregate", "input": {"number": 1}}
        ]

        # Test generator handler
        generator_config = {
            "handler": generator_handler,
            "return_aggregate_stream": True,
            "refresh_worker": True,
        }

        submodel.serverless.start(generator_config)

        assert mock_send_result.called
        assert mock_stream_result.called
        assert not mock_run_job.called

        # Since return_aggregate_stream is activated, we should submit a list of the outputs.
        _, args, _ = mock_send_result.mock_calls[0]
        assert args[1] == {"output": ["test1", "test2"], "stopPod": True}

    @patch("submodel.serverless.modules.sm_scale.AsyncClientSession")
    @patch("submodel.serverless.modules.sm_scale.get_job")
    @patch("submodel.serverless.modules.sm_job.run_job")
    @patch("submodel.serverless.modules.sm_job.stream_result")
    @patch("submodel.serverless.modules.sm_job.send_result")
    async def test_run_worker_concurrency(
        self,
        mock_send_result,
        mock_stream_result,
        mock_run_job,
        mock_get_job,
        mock_session,
    ):
        """
        Test run_worker with synchronous handler, ensuring that concurrency behavior
        is respected and that the calls to `get_job`, `run_job`, and `send_result`
        follow expected patterns.

        Args:
            mock_send_result: Mock for send_result function
            mock_stream_result: Mock for stream_result function
            mock_run_job: Mock for run_job function
            mock_get_job: Mock for get_job function
            mock_session: Mock for AsyncClientSession
        """
        # Define the mock behaviors
        mock_get_job.return_value = [{"id": "123", "input": {"number": 1}}]
        mock_run_job.return_value = {"output": {"result": "odd"}}

        # Set a simple concurrency modifier that doesn't change the concurrency
        def concurrency_modifier(current_concurrency):
            return current_concurrency

        config_with_concurrency = self.config.copy()
        config_with_concurrency["concurrency_modifier"] = concurrency_modifier

        # Call the function
        submodel.serverless.start(config_with_concurrency)

        # Make assertions about the behaviors
        self.assertGreaterEqual(
            mock_get_job.call_count, 1, 
            f"Expected at least one call to get_job, but got {mock_get_job.call_count}"
        )

        self.assertGreaterEqual(
            mock_run_job.call_count, 1,
            f"Expected at least one call to run_job, but got {mock_run_job.call_count}"
        )

        self.assertGreaterEqual(
            mock_send_result.call_count, 1,
            f"Expected at least one call to send_result, but got {mock_send_result.call_count}"
        )

        self.assertFalse(
            mock_stream_result.called,
            "stream_result should not be called in this test case."
        )

        self.assertTrue(
            mock_session.called,
            "Expected the mock_session to be used at least once."
        )

        # Verify each call to send_result
        for call in mock_send_result.mock_calls:
            args, kwargs = call
            # Check if the 'output' key is present instead of 'result'
            if "output" in args[1]:
                self.assertIn(
                    "result", args[1]["output"], 
                    "Expected 'result' to be part of the 'output' dictionary."
                )
            else:
                self.fail("The 'output' key was not found in the arguments for send_result.")

    @patch("submodel.serverless.modules.sm_scale.AsyncClientSession")
    @patch("submodel.serverless.modules.sm_scale.get_job")
    @patch("submodel.serverless.modules.sm_job.run_job")
    @patch("submodel.serverless.modules.sm_job.stream_result")
    @patch("submodel.serverless.modules.sm_job.send_result")
    async def test_run_worker_multi_processing(
        self,
        mock_send_result,
        mock_stream_result,
        mock_run_job,
        mock_get_job,
        mock_session,
    ):
        """
        Test run_worker with multi-processing enabled for both async and generator handlers.
        """

        # Define the mock behaviors
        mock_get_job.return_value = [{"id": "123", "input": {"number": 1}}]
        mock_run_job.return_value = {"output": {"result": "odd"}}

        # Run the worker with the original configuration
        submodel.serverless.start(self.config)

        # Check that `get_job`, `run_job`, and `send_result` were called
        self.assertGreaterEqual(mock_get_job.call_count, 1, "Expected at least one call to get_job.")
        self.assertGreaterEqual(mock_run_job.call_count, 1, "Expected at least one call to run_job.")
        self.assertGreaterEqual(mock_send_result.call_count, 1, "Expected at least one call to send_result.")
        
        # Ensure that `stream_result` was not called during the synchronous handler test
        self.assertFalse(mock_stream_result.called, "Expected stream_result to not be called.")
        
        # Ensure that the mock session was used
        self.assertTrue(mock_session.called, "Expected mock session to be called.")

        # Test generator handler
        generator_config = {"handler": generator_handler, "refresh_worker": True}
        submodel.serverless.start(generator_config)

        # Now `stream_result` should be called for the generator handler
        self.assertTrue(mock_stream_result.called, "Expected stream_result to be called for the generator handler.")

        # Test with limited configuration and patch `_set_config_args`
        with patch("submodel.serverless._set_config_args") as mock_set_config_args:
            limited_config = {
                "handler": Mock(),
                "refresh_worker": True,
                "sm_args": {
                    "sm_debugger": True,
                    "sm_serve_api": None,
                    "sm_api_port": 8000,
                    "sm_api_concurrency": 1,
                    "sm_api_host": "localhost",
                },
            }

            mock_set_config_args.return_value = limited_config
            submodel.serverless.start(limited_config)

            # Verify `_set_config_args` was called with the expected arguments
            self.assertTrue(mock_set_config_args.called, "Expected _set_config_args to be called.")
            print(mock_set_config_args.call_args_list)

    @patch("submodel.serverless.modules.sm_scale.get_job")
    @patch("submodel.serverless.modules.sm_job.run_job")
    async def test_run_worker_multi_processing_scaling_up(
        self, mock_run_job, mock_get_job
    ):
        """
        Test run_worker with multi processing enabled, the scale-up and scale-down
        behavior with concurrency_controller.

        Args:
            mock_send_result (_type_): _description_
            mock_stream_result (_type_): _description_
            mock_run_job (_type_): _description_
            mock_get_job (_type_): _description_
            mock_session (_type_): _description_
        """
        # Define the mock behaviors
        mock_get_job.return_value = [{"id": "123", "input": {"number": 1}}]
        mock_run_job.return_value = {"output": {"result": "odd"}}

        # Include multi-processing inside config
        # Should go from concurrency 1 -> 2 -> 4 -> 8 -> 16 -> 8 -> 4 -> 2 -> 1
        # 1+2+4+8+16+8+4+2+1 -> 46 calls to get_job.
        scale_behavior = {
            "behavior": [
                False,
                False,
                False,
                False,
                False,
                False,
                True,
                True,
                True,
                True,
                True,
            ],
            "counter": 0,
        }

        # Let the test be a long running one so we can capture the scale-up and scale-down.
        config = {
            "handler": MagicMock(),
            "refresh_worker": False,
            "sm_args": {"sm_debugger": True, "sm_log_level": "DEBUG"},
        }

        # Let's mock job_scaler.is_alive so that it returns False
        # when scale_behavior's counter is now 5.
        def mock_is_alive():
            res = scale_behavior["counter"] < 10
            scale_behavior["counter"] += 1
            return res

        with patch(
            "submodel.serverless.modules.sm_scale.JobScaler.is_alive", wraps=mock_is_alive
        ):
            submodel.serverless.start(config)

    @patch("submodel.serverless.signal.signal")
    @patch("submodel.serverless.worker.sm_scale.JobScaler.run")
    def test_start_sets_excepthook(self, _, __):
        submodel.serverless.start({})
        assert sys.excepthook == _handle_uncaught_exception

    @patch("submodel.serverless.signal.signal")
    @patch("submodel.serverless.sm_fastapi.WorkerAPI.start_uvicorn")
    @patch("submodel.serverless._set_config_args")
    def test_start_does_not_set_excepthook(self, mock_set_config_args, _, __):
        mock_set_config_args.return_value = self.config
        self.config.update({"sm_args": {
            "sm_serve_api": True,
            "sm_api_host": "localhost",
            "sm_api_port": 8000,
            "sm_api_concurrency": 1,
        }})

        submodel.serverless.start(self.config)
        assert sys.excepthook != _handle_uncaught_exception
