# submodel CLI

Note: This CLI is not the same as submodelctl and provides a different set of features.

```bash
# Auth
submodel config

submodel ssh list-keys
submodel ssh add-key

submodel pod list
submodel pod create
submodel pod connect

submodel exec python file.py
```

## Overview

```bash
submodel --help
```

### Configure

```bash
$ submodel config
Profile [default]:
submodel API Key [None]: YOUR_submodel_API_KEY
```

### Launch Pod

```bash
submodel launch --help
submodel launch pod --template-file template.yaml
```

### Launch Endpoint

```bash
submodel launch endpoint --help
submodel launch endpoint --template-file template.yaml
```
