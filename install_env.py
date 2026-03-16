import os
import subprocess
import platform

def run_command_with_log(command, log_callback):
    process = subprocess.Popen(
        command,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True,
        bufsize=1
    )
    
    for line in iter(process.stdout.readline, ''):
        clean_line = line.strip()
        if clean_line != "":
            if log_callback != None:
                log_callback(clean_line)
                
    process.wait()
    
    if process.returncode == 0:
        return True
    return False

def get_micromamba(plugin_dir):
    system = platform.system().lower()
    arch = platform.machine().lower()
    
    mamba_base_dir = os.path.join(plugin_dir, "mamba")
    exe_path = ""
    
    if system == "windows":
        exe_path = os.path.join(mamba_base_dir, "Windows", "micromamba.exe")
        
    if system == "darwin":
        if arch == "arm64":
            exe_path = os.path.join(mamba_base_dir, "macOS_silicon", "bin", "micromamba")
        if arch != "arm64":
            exe_path = os.path.join(mamba_base_dir, "macOS_intel", "bin", "micromamba")
            
    if system == "linux":
        if arch == "aarch64" or arch == "arm64":
            exe_path = os.path.join(mamba_base_dir, "linux_arm64", "bin", "micromamba")
        if arch != "aarch64" and arch != "arm64":
            exe_path = os.path.join(mamba_base_dir, "linux_intel", "bin", "micromamba")
            
    return exe_path

def setup_flair_environment(plugin_dir,mamba_exe, env_dir,log_callback=None,progress_callback=None):

    req_file = os.path.join(plugin_dir, "vendor", "FLAIR-1", "flair.egg-info", "requires.txt")
    
    dependencies = []
    if progress_callback != None:
            progress_callback(10)
    
    if os.path.exists(req_file):
        with open(req_file, 'r') as file:
            for line in file:
                clean_line = line.strip()
                if clean_line != "":
                    dependencies.append(clean_line)
                    
    if len(dependencies) > 0:
        base_cmd = [
            mamba_exe, "create", "-y", "-p", env_dir, 
            "-c", "conda-forge", "python=3.10", "pip", "gdal"
        ]
        run_command_with_log(base_cmd, log_callback)

        if progress_callback != None:
            progress_callback(50)
        
        pip_exe = os.path.join(env_dir, "bin", "pip")
        
        if os.name == "nt": #windows
            pip_exe = os.path.join(env_dir, "Scripts", "pip.exe")
            
        pip_cmd = [pip_exe, "install"] + dependencies
        run_command_with_log(pip_cmd, log_callback)
        if progress_callback != None:
            progress_callback(100)

if __name__ == "__main__":
    current_dir = os.path.dirname(os.path.abspath(__file__))
    setup_flair_environment(current_dir)