import os
import shutil

site_root=os.path.realpath(os.path.dirname(__file__))
# Ruta de la carpeta de inicio de Windows (shell:startup)
carpeta_inicio = os.path.join(os.environ["APPDATA"], "Microsoft", "Windows", "Start Menu", "Programs", "Startup")
# ------------------------------------------
# Crear el bat
bat_content=f'''
@echo off
cscript //nologo "{site_root}\\ocultar_script.vbs"
'''
with open(f"{carpeta_inicio}\\run_project.bat", "w") as archivo_bat:
    archivo_bat.write(bat_content)
