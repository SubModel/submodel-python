# Handling Errors

```Python
import submodel

try:
    # Use submodel to make a request
except submodel.error.AuthenticationError as err:
    # Authentication with the API failed
```
