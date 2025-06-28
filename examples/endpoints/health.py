""" Example of getting the health of an endpoint. """

import submodel

# Set your global API key with `submodel config` or uncomment the line below:
# submodel.api_key = "YOUR_SUBMODEL_API_KEY"

endpoint = submodel.Endpoint("gwp4kx5yd3nur1")

endpoint_health = endpoint.health()

print(endpoint_health)
