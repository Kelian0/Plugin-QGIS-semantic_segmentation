import os
import subprocess
import platform

def run_command_with_log(command, log_callback, log_file_path=None, custom_env=None):
    creation_flags = 0
    
    if os.name == "nt":
        creation_flags = subprocess.CREATE_NO_WINDOW
    
    process = subprocess.Popen(
        command,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True,
        bufsize=1,
        env=custom_env,
        creationflags=creation_flags
    )
    
    if log_file_path != None:
        log_file = open(log_file_path, "a", encoding="utf-8")
        
    for line in iter(process.stdout.readline, ''):
        clean_line = line.strip()
        if clean_line != "":
            if log_callback != None:
                log_callback(clean_line)
            if log_file_path != None:
                log_file.write(clean_line + "\n")
                log_file.flush()
                
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
        exe_path = os.path.join(mamba_base_dir, "Windows","Library","bin", "micromamba.exe")
        
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
    log_path = os.path.join(plugin_dir, "install_log.txt")

    clean_env = os.environ.copy()
        
    if "PYTHONPATH" in clean_env:
        del clean_env["PYTHONPATH"]
        
    if "PYTHONHOME" in clean_env:
        del clean_env["PYTHONHOME"]
    
    dependencies = []
    
    if progress_callback != None:
        progress_callback(10)
    
    if os.path.exists(log_path):
        os.remove(log_path)
            
    if os.path.exists(req_file):
        with open(req_file, 'r') as file:
            for line in file:
                clean_line = line.strip()
                if clean_line != "":
                    dependencies.append(clean_line)
                    
    if len(dependencies) == 0:
        return False

    base_cmd = [
        mamba_exe, "create", "-y", "-p", env_dir, 
        "-c", "conda-forge", "--override-channels", 
        "python=3.10", "pip", "gdal"
    ]
    
    mamba_ok = run_command_with_log(base_cmd, log_callback, log_path, clean_env)
    
    if mamba_ok == False:
        if log_callback != None:
            log_callback("Error: Failed to create Conda environment. Check install_log.txt")
        return False

    if progress_callback != None:
        progress_callback(50)
    
    python_exe = os.path.join(env_dir, "bin", "python")
    
    if os.name == "nt":
        python_exe = os.path.join(env_dir, "python.exe")
        
    pip_cmd = [python_exe, "-m", "pip", "install"] + dependencies
    
    pip_ok = run_command_with_log(pip_cmd, log_callback, log_path, clean_env)
    
    if pip_ok == False:
        if log_callback != None:
            log_callback("Error: Failed to install pip dependencies. Check install_log.txt")
        return False
        
    if progress_callback != None:
        progress_callback(100)
        
    return True

if __name__ == "__main__":
    current_dir = os.path.dirname(os.path.abspath(__file__))
    setup_flair_environment(current_dir)