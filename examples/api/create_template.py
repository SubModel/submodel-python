""" Example of creating a template with the SubModel API. """

import submodel

# Set your global API key with `submodel config` or uncomment the line below:
# submodel.api_key = "YOUR_SUBMODEL_API_KEY"

try:

    new_template = submodel.create_template(name="test", image_name="submodel/base:0.1.0")

    print(new_template)

except submodel.error.QueryError as err:
    print(err)
    print(err.query)
