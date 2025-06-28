""" A template for a handler file. """

import submodel


def handler(job):
    """
    This is the handler function for the job.
    """
    job_input = job["input"]
    name = job_input.get("name", "World")
    return f"Hello, {name}!"


submodel.serverless.start({"handler": handler})
