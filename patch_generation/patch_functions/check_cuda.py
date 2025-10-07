import torch
def check_cuda():  
    # Check the GPU availability
    if torch.cuda.is_available():
        print(f"\nGPU Name: {torch.cuda.get_device_name(0)}")
        print(f"GPU Count: {torch.cuda.device_count()}")
    else:
        print("\nsNo GPU found.")
