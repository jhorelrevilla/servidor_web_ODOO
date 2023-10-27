import subprocess
import os


def run_command(comando):
    proceso = subprocess.Popen(
        comando, 
        shell=True, 
        stdout=subprocess.PIPE, 
        stderr=subprocess.PIPE, 
        stdin=subprocess.PIPE, 
        text=True
    )
    salida, error = proceso.communicate()

    return salida, error


site_root=os.path.realpath(os.path.dirname(__file__))
env_dir=os.path.join(site_root,'env','Scripts','activate.bat')
app_dir=os.path.join(site_root,'app.py')
# Carga el entorno virtual
run_command(f"{env_dir}")
# Ejecuta el codigo
run_command(f"python {env_dir}")

