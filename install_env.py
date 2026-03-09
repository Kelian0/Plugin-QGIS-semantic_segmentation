import os
import subprocess
import shutil

def find_conda_executable():
    conda_exe = shutil.which("conda")
    if conda_exe:
        return conda_exe
        
    common_paths = [
        os.path.expanduser("~/miniconda3/bin/conda"),
        os.path.expanduser("~/miniconda3/condabin/conda"),
        os.path.expanduser("~/anaconda3/bin/conda"),
        os.path.expanduser("~/anaconda3/condabin/conda"),
        "/opt/conda/bin/conda"
    ]
    
    for path in common_paths:
        if os.path.exists(path):
            return path
            
    raise FileNotFoundError("Conda executable not found. Please ensure Miniconda/Anaconda is installed.")

def setup_flair_environment(plugin_dir):
    plugin_dir = os.path.realpath(plugin_dir)
    env_dir = os.path.join(plugin_dir, "flair_env")
    flair_repo_dir = os.path.join(plugin_dir, "vendor", "FLAIR-1")
    conda_exe = find_conda_executable()

    if os.path.exists(env_dir):
        shutil.rmtree(env_dir, ignore_errors=True)

    print("Creating Conda environment...")
    subprocess.run(
        [conda_exe, "create", "-y", "-p", env_dir, "-c", "conda-forge", "python=3.11"], 
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