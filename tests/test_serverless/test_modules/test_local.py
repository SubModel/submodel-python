""" Tests for sm_local.py """

from unittest import IsolatedAsyncioTestCase
from unittest.mock import mock_open, patch

from submodel.serverless.modules import sm_local


class TestRunLocal(IsolatedAsyncioTestCase):
    """Tests for run_local function"""

    @patch(
        "submodel.serverless.modules.sm_local.run_job", return_value={"result": "success"}
    )
    @patch("builtins.open", new_callable=mock_open, read_data='{"input": "test"}')
    async def test_run_local_with_test_input(self, mock_file, mock_run):
        """
        Test run_local function with test_input in sm_args
        """
        config = {
            "handler": "handler",
            "sm_args": {
                "test_input": {"input": "test", "id": "test_id"},
                "test_output": {"result": "success"},
            },
        }
        with self.assertRaises(SystemExit) as sys_exit:
            await sm_local.run_local(config)
            self.assertEqual(sys_exit.exception.code, 0)

        config["sm_args"]["test_output"] = {"result": "fail"}
        with self.assertRaises(SystemExit) as sys_exit:
            await sm_local.run_local(config)
            self.assertEqual(sys_exit.exception.code, 1)

        assert mock_file.called is False
        assert mock_run.called

    @patch("submodel.serverless.modules.sm_local.run_job", return_value={})
    @patch("builtins.open", new_callable=mock_open, read_data='{"input": "test"}')
    async def test_run_local_with_test_input_json(self, mock_file, mock_run):
        """
        Test run_local function with test_input.json
        """
        config = {"handler": "handler", "sm_args": {}}
        with patch("os.path.exists", return_value=True):
            with self.assertRaises(SystemExit) as sys_exit:
                await sm_local.run_local(config)
            self.assertEqual(sys_exit.exception.code, 0)

        assert mock_file.called
        assert mock_run.called

    @patch(
        "submodel.serverless.modules.sm_local.run_job",
        return_value={"error": "test_error"},
    )
    @patch("builtins.open", new_callable=mock_open, read_data='{"input": "test"}')
    async def test_run_local_with_error(self, mock_file, mock_run):
        """
        Test run_local function when run_job returns an error
        """
        config = {
            "handler": "handler",
            "sm_args": {"test_input": {"input": "test", "id": "test_id"}},
        }
        with self.assertRaises(SystemExit) as sys_exit:
            await sm_local.run_local(config)
        self.assertEqual(sys_exit.exception.code, 1)

        assert mock_file.called is False
        assert mock_run.called

    async def test_run_local_without_test_input_json(self):
        """
        Test run_local function without test_input.json
        """
        config = {"handler": "handler", "sm_args": {}}
        with patch("os.path.exists", return_value=False):
            with self.assertRaises(SystemExit) as sys_exit:
                await sm_local.run_local(config)
            self.assertEqual(sys_exit.exception.code, 1)

    @patch("submodel.serverless.modules.sm_local.run_job", return_value={})
    @patch("builtins.open", new_callable=mock_open, read_data='{"not_input": "test"}')
    async def test_run_local_without_input(self, mock_file, mock_run):
        """
        Test run_local function without input in test_input.json
        """
        config = {"handler": "handler", "sm_args": {}}
        with patch("os.path.exists", return_value=True):
            with self.assertRaises(SystemExit) as sys_exit:
                await sm_local.run_local(config)
            self.assertEqual(sys_exit.exception.code, 1)

        assert mock_file.called
        assert mock_run.called is False
