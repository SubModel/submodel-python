""" User-Agent for Submodel-Python-SDK """

import os
import platform

from submodel.version import __version__ as submodel_version


def construct_user_agent():
    """Constructs the User-Agent string for the Submodel-Python-SDK

    Returns:
        str: The User-Agent string in the format:
        Submodel-Python-SDK/0.1.0 (Linux 5.4.0-54-generic; x86_64) Language/Python 3.8.5
    """

    integration_method = os.getenv("SUBMODEL_UA_INTEGRATION")

    parts = [
        f"Submodel-Python-SDK/{submodel_version}",
        f"({platform.system()} {platform.release()}; {platform.machine()})",
        f"Language/Python {platform.python_version()}",
    ]

    if integration_method:
        parts.append(f"Integration/{integration_method}")

    return " ".join(parts)


USER_AGENT = construct_user_agent()
