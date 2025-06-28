""" Example of creating an endpoint with the SubModel API. """

import submodel

# Set your global API key with `submodel config` or uncomment the line below:
# submodel.api_key = "YOUR_SUBMODEL_API_KEY"

try:

    new_template = submodel.create_template(
        name="test", image_name="submodel/base:0.4.4", is_serverless=True
    )

    print(new_template)

    new_endpoint = submodel.create_endpoint(
        name="test",
        template_id=new_template["id"],
        gpu_ids="AMPERE_16",
        workers_min=0,
        workers_max=1,
        flashboot=True,
    )

    print(new_endpoint)

except submodel.error.QueryError as err:
    print(err)
    print(err.query)
