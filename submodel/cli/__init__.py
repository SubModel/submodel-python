""" Allows the CLI to be imported as a module. """

import threading

from .groups import config, ssh

STOP_EVENT = threading.Event()


# --------------------------- submodel.toml Defaults --------------------------- #
BASE_DOCKER_IMAGE = "submodel/base:0.4.3-cuda{cuda_version}"
GPU_TYPES = [
    "NVIDIA RTX A4000",
    "NVIDIA RTX A4500",
    "NVIDIA RTX A5000",
    "NVIDIA GeForce RTX 3090",
    "NVIDIA RTX A6000",
]
ENV_VARS = {
    "POD_INACTIVITY_TIMEOUT": "120",
    "SUBMODEL_DEBUG_LEVEL": "debug",
    "UVICORN_LOG_LEVEL": "warning",
}
