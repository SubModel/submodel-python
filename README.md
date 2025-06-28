<div align="center">
<h1>submodel | Python Library </h1>

[![PyPI Package](https://badge.fury.io/py/submodel.svg)](https://badge.fury.io/py/submodel)
&nbsp;
[![Downloads](https://static.pepy.tech/personalized-badge/submodel?period=total&units=international_system&left_color=grey&right_color=blue&left_text=Downloads)](https://pepy.tech/project/submodel)

[![CI | End-to-End submodel Python Tests](https://github.com/submodel/submodel-python/actions/workflows/CI-e2e.yml/badge.svg)](https://github.com/submodel/submodel-python/actions/workflows/CI-e2e.yml)

[![CI | Code Quality](https://github.com/submodel/submodel-python/actions/workflows/CI-pylint.yml/badge.svg)](https://github.com/submodel/submodel-python/actions/workflows/CI-pylint.yml)
&nbsp;
[![CI | Unit Tests](https://github.com/submodel/submodel-python/actions/workflows/CI-pytests.yml/badge.svg)](https://github.com/submodel/submodel-python/actions/workflows/CI-pytests.yml)
&nbsp;
[![CI | CodeQL](https://github.com/submodel/submodel-python/actions/workflows/CI-codeql.yml/badge.svg)](https://github.com/submodel/submodel-python/actions/workflows/CI-codeql.yml)

</div>

Welcome to the official Python library for submodel API &amp; SDK.

## Table of Contents

- [Table of Contents](#table-of-contents)
- [💻 | Installation](#--installation)
- [⚡ | Serverless Worker (SDK)](#--serverless-worker-sdk)
  - [Quick Start](#quick-start)
  - [Local Test Worker](#local-test-worker)
- [📚 | API Language Library (API Wrapper)](#--api-language-library-wrapper)
  - [Endpoints](#endpoints)
  - [GPU Cloud (Pods)](#gpu-cloud-pods)
- [📁 | Directory](#--directory)
- [🤝 | Community and Contributing](#--community-and-contributing)

## 💻 | Installation

```bash
# Install the latest release version
pip install submodel

# or

# Install the latest development version (main branch)
pip install git+https://github.com/submodel/submodel-python.git
```

*Python 3.8 or higher is required to use the latest version of this package.*

## | Serverless Worker (SDK)

This python package can also be used to create a serverless worker that can be deployed to submodel as a custom endpoint API.

### Quick Start

Create a python script in your project that contains your model definition and the submodel worker start code. Run this python code as your default container start command:

```python
# my_worker.py

import submodel

def is_even(job):

    job_input = job["input"]
    the_number = job_input["number"]

    if not isinstance(the_number, int):
        return {"error": "Silly human, you need to pass an integer."}

    if the_number % 2 == 0:
        return True

    return False

submodel.serverless.start({"handler": is_even})
```

Make sure that this file is ran when your container starts. This can be accomplished by calling it in the docker command when you set up a template at [submodel.io/console/serverless/user/templates](https://www.submodel.io/console/serverless/user/templates) or by setting it as the default command in your Dockerfile.

See our [blog post](https://www.submodel.io/blog/serverless-create-a-basic-api) for creating a basic Serverless API, or view the [details docs](https://docs.submodel.io/serverless-ai/custom-apis) for more information.

### Local Test Worker

You can also test your worker locally before deploying it to submodel. This is useful for debugging and testing.

```bash
python my_worker.py --sm_serve_api
```

## 📚 | API Language Library (API Wrapper)

When interacting with the submodel API you can use this library to make requests to the API.

```python
import submodel

submodel.api_key = "your_submodel_api_key_found_under_settings"
```

### Endpoints

You can interact with submodel endpoints via a `run` or `run_sync` method.

```python
endpoint = submodel.Endpoint("ENDPOINT_ID")

run_request = endpoint.run(
    {"your_model_input_key": "your_model_input_value"}
)

# Check the status of the endpoint run request
print(run_request.status())

# Get the output of the endpoint run request, blocking until the endpoint run is complete.
print(run_request.output())
```

```python
endpoint = submodel.Endpoint("ENDPOINT_ID")

run_request = endpoint.run_sync(
    {"your_model_input_key": "your_model_input_value"}
)

# Returns the job results if completed within 90 seconds, otherwise, returns the job status.
print(run_request )
```

### GPU Cloud (Pods)

```python
import submodel

submodel.api_key = "your_submodel_api_key_found_under_settings"

# Get all my pods
pods = submodel.get_pods()

# Get a specific pod
pod = submodel.get_pod(pod.id)

# Create a pod with GPU
pod = submodel.create_pod("test", "submodel/stack", "NVIDIA GeForce RTX 3070")

# Create a pod with CPU
pod = submodel.create_pod("test", "submodel/stack", instance_id="cpu3c-2-4")

# Stop the pod
submodel.stop_pod(pod.id)

# Resume the pod
submodel.resume_pod(pod.id)

# Terminate the pod
submodel.terminate_pod(pod.id)
```

## 📁 | Directory

```BASH
.
├── docs               # Documentation
├── examples           # Examples
├── submodel             # Package source code
│   ├── api_wrapper    # Language library - API
│   ├── cli            # Command Line Interface Functions
│   ├── endpoint       # Language library - Endpoints
│   └── serverless     # SDK - Serverless Worker
└── tests              # Package tests
```

## 🤝 | Community and Contributing

We welcome both pull requests and issues on [GitHub](https://github.com/submodel/submodel-python). Bug fixes and new features are encouraged, but please read our [contributing guide](CONTRIBUTING.md) first.

<div align="center">

<a target="_blank" href="https://discord.gg/mXEXA3MSwD">![Discord Banner 2](https://discordapp.com/api/guilds/1340209190425333815/widget.png?style=banner2)</a>

</div>
