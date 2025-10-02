import torch
import numpy as np
import random
def set_seeds(seed=42):
    # Set the seed for PyTorch
    torch.manual_seed(seed)

    # If you are using CUDA
    if torch.cuda.is_available():
        torch.cuda.manual_seed(seed)
        torch.cuda.manual_seed_all(seed)  # for all GPUs

    # Set the seed for NumPy
    np.random.seed(seed)

    # Set the seed for Python's built-in random module
    random.seed(seed)
