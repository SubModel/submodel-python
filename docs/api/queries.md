## get_gpus

```python
import submodel

submodel.api_key = "your_submodel_api_key"

gpus = submodel.get_gpus()

for gpu in gpus:
    print(gpu)
```

### get_gpus Output

```json
{'id': 'NVIDIA A100 80GB PCIe', 'displayName': 'A100 80GB', 'memoryInGb': 80}
{'id': 'NVIDIA A100-SXM4-80GB', 'displayName': 'A100 SXM 80GB', 'memoryInGb': 80}
{'id': 'NVIDIA A30', 'displayName': 'A30', 'memoryInGb': 24}
```

## get_gpu

```python
gpu_id = "NVIDIA A100 80GB PCIe"
gpu = submodel.get_gpu(gpu_id)

print(gpu)
```

### get_gpu Output

```json
{'id': 'NVIDIA A100 80GB PCIe', 'displayName': 'A100 80GB', 'memoryInGb': 80, 'secureCloud': True, 'communityCloud': True, 'lowestPrice': {'minimumBidPrice': 1.158, 'uninterruptablePrice': 1.89}}
```
