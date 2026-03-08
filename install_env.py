import os
import subprocess
import shutil

def setup_flair_environment(plugin_dir):
    plugin_dir = os.path.realpath(plugin_dir)
    env_dir = os.path.join(plugin_dir, "flair_env")
    flair_repo_dir = os.path.join(plugin_dir, "vendor", "FLAIR-1")

    if os.path.exists(env_dir):
        shutil.rmtree(env_dir, ignore_errors=True)

    print("Creating Conda environment...")
    subprocess.run(
        ["conda", "create", "-y", "-p", env_dir, "-c", "conda-forge", "python=3.11"], 
        check=True
    )

    python_exe = os.path.join(env_dir, "python.exe") if os.name == 'nt' else os.path.join(env_dir, "bin", "python")

    print("Installing FLAIR dependencies and downgraded setuptools...")
    subprocess.run(
        [python_exe, "-m", "pip", "install", "setuptools<70.0.0", "-e", "."], 
        cwd=flair_repo_dir, 
        check=True
    )

    print("Installing CPU version of PyTorch...")
    subprocess.run([
        python_exe, "-m", "pip", "install", 
        "torch>=2.0.0", "torchvision", 
        "--extra-index-url", "https://download.pytorch.org/whl/cpu"
    ], check=True)

    print("Environment setup completed successfully.")
    return python_exe

if __name__ == "__main__":
    current_dir = os.path.dirname(os.path.abspath(__file__))
    setup_flair_environment(current_dir)