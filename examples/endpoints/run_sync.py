"""
Example of calling an endpoint using the SubModel Python Language Library.
"""

import submodel

# Set your global API key with `submodel config` or uncomment the line below:
# submodel.api_key = "YOUR_SUBMODEL_API_KEY"

endpoint = submodel.Endpoint("sdxl")  # Where "sdxl" is the endpoint ID

try:
    # Run the endpoint synchronously, blocking until the endpoint run is complete.
    run_request = endpoint.run_sync(
        {"input": {"prompt": "a photo of a horse the size of a Boeing 787"}},
        timeout=60,  # Seconds
    )

    print(run_request)
except TimeoutError as err:
    print("Job timed out.")
