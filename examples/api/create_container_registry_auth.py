""" Example of creating a container registry auth with the SubModel API. """

import submodel

# Set your global API key with `submodel config` or uncomment the line below:
# submodel.api_key = "YOUR_SUBMODEL_API_KEY"

try:
    new_container_registry_auth = submodel.create_container_registry_auth(
        name="test-container-registry-auth-name",
        username="test-username",
        password="test-password",
    )

    print(new_container_registry_auth)

except submodel.error.QueryError as err:
    print(err)
    print(err.query)
