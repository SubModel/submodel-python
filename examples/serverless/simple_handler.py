""" Simple Handler

To setup a local API server, run the following command:
python simple_handler.py --sm_serve_api
"""

import submodel


def handler(job):
    """Simple handler"""
    job_input = job["input"]

    return f"Hello {job_input['name']}!"


submodel.serverless.start({"handler": handler})
