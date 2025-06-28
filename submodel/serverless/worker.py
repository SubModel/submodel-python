"""
submodel | serverless | worker_loop.py
Called to convert a container into a worker pod for the submodel serverless platform.
"""

import asyncio
import os
from typing import Any, Dict

from submodel.serverless.modules import sm_logger, sm_local, sm_ping, sm_scale

log = sm_logger.SubModelLogger()
heartbeat = sm_ping.Heartbeat()


def _is_local(config) -> bool:
    """Returns True if the worker is running locally, False otherwise."""
    if config["sm_args"].get("test_input", None):
        return True

    if os.environ.get("SUBMODEL_WEBHOOK_GET_JOB", None) is None:
        return True

    return False


# ------------------------- Main Worker Running Loop ------------------------- #
def run_worker(config: Dict[str, Any]) -> None:
    """
    Starts the worker loop for multi-processing.

    This function is called when the worker is running on SubModel. This function
    starts a loop that runs indefinitely until the worker is killed.

    Args:
        config (Dict[str, Any]): Configuration parameters for the worker.
    """
    # Start pinging SubModel to show that the worker is alive.
    heartbeat.start_ping()

    # Create a JobScaler responsible for adjusting the concurrency
    job_scaler = sm_scale.JobScaler(config)
    job_scaler.start()


def main(config: Dict[str, Any]) -> None:
    """
    Checks if the worker is running locally or on SubModel.
    If running locally, the test job is run and the worker exits.
    If running on SubModel, the worker loop is created.
    """
    if _is_local(config):
        asyncio.run(sm_local.run_local(config))

    else:
        run_worker(config)
