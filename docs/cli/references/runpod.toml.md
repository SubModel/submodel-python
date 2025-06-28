# Project File

Project files are stored as a `submodel.toml` file in the root of your project. This file contains all the information needed to run your project on the submodel platform.

## Example

```toml
# submodel Project Configuration

title = "My Project"

[project]
uuid = "00000000"
name = "My Project"
base_image = "submodel/base:0.0.0"
gpu_types = ["NVIDIA RTX 3090"]
gpu_count = 1
storage_id = "00000000"
volume_mount_path = "/submodel-volume"
ports = "8080/http, 22/tcp"
container_disk_size_gb = 10

[project.env_vars]
VAR_NAME_1 = "value1"
VAR_NAME_2 = "value2"


[template]
model_type = "default"
model_name = "None"

[runtime]
python_version = "3.10"
handler_path = "handler.py"
requirements_path = "requirements.txt"
```
