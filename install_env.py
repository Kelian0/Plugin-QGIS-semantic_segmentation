import os
import subprocess
import venv
import sys

def setup_flair_environment(plugin_dir):
    """
    Create a virtual env and install python dependencies 
    """
    env_dir = os.path.join(plugin_dir, "flair_env")
    
    # path to python
    if os.name == 'nt':  # Windows
        python_exe = os.path.join(env_dir, "Scripts", "python.exe")
    else:                # Mac / Linux
        python_exe = os.path.join(env_dir, "bin", "python")

    # creating the env if it doesn't exist already
    if not os.path.exists(env_dir):
        print("Creating env...")
        venv.create(env_dir, with_pip=True)
    else:
        print("The env already exists")

    # updating pip
    subprocess.run([python_exe, "-m", "pip", "install", "--upgrade", "pip"], check=True)

    # list of dependencies
    dependencies = [
        "rasterio",
        "pyyaml",
        "tqdm",
        "segmentation-models-pytorch",
        "pytorch-lightning"
    ]

    # Installation of PyTorch (CPU version by default)
    subprocess.run([
        python_exe, "-m", "pip", "install", 
        "torch", "torchvision", 
        "--index-url", "https://download.pytorch.org/whl/cpu"
    ], check=True)

    # Installation of the other dependencies
    print("Installation of other dependencies...")
    subprocess.run([python_exe, "-m", "pip", "install"] + dependencies, check=True)

    print("Successful Installation")
    return python_exe