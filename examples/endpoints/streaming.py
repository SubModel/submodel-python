""" Example of streaming data from an endpoint. """

import submodel

# Set your global API key with `submodel config` or uncomment the line below:
# submodel.api_key = "YOUR_SUBMODEL_API_KEY"

endpoint = submodel.Endpoint("gwp4kx5yd3nur1")

run_request = endpoint.run(
    {
        "input": {
            "mock_return": ["a", "b", "c", "d", "e", "f", "g"],
            "mock_delay": 1,
        }
    }
)

for output in run_request.stream():
    print(output)
