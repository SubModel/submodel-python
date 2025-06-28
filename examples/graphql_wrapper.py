"""'
Wrapper for the SubModel API
"""

import time

import submodel

submodel.api_key = "YOUR_SUBMODEL_API_KEY"

# Get all GPUs
gpus = submodel.get_gpus()
print(gpus)

# Get a specific GPU
gpu = submodel.get_gpu("NVIDIA GeForce RTX 3070")
print(gpu)

# Create a pod
pod = submodel.create_pod("test", "submodel/stack", "NVIDIA GeForce RTX 3070")
print(pod)

# Pause while the pod is being created
print("Waiting for pod to be created...")
time.sleep(10)

# Stop a pod
pod = submodel.stop_pod(pod["id"])
print(pod)

# Pause while the pod is being stopped
print("Waiting for pod to be stopped...")
time.sleep(10)

# Resume a pod
pod = submodel.resume_pod(pod["id"], 1)
print(pod)

# Pause while the pod is being resumed
print("Waiting for pod to be resumed...")
time.sleep(10)

# Terminate a pod
submodel.terminate_pod(pod["id"])
