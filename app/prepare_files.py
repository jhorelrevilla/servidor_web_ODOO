import os
import shutil

site_root=os.path.realpath(os.path.dirname(__file__))
# Ruta de la carpeta de inicio de Windows (shell:startup)
carpeta_inicio = os.path.join(os.environ["APPDATA"], "Microsoft", "Windows", "Start Menu", "Programs", "Startup")
# ------------------------------------------
# Crear el vbs
vbs_code = f'''
Set WshShell = CreateObject("WScript.Shell")
WshShell.Run chr(34) & "{site_root}\\run_server.bat" & Chr(34), 0
Set WshShell = Nothing
'''
with open(f"{carpeta_inicio}\\ocultar_script.vbs", "w") as archivo_vbs:
    archivo_vbs.write(vbs_code)
# ------------------------------------------
# Crear el bat
bat_content=f'''
@echo off
cscript //nologo ocultar_script.vbs
'''
with open(f"{carpeta_inicio}\\run_project.bat", "w") as archivo_bat:
    archivo_bat.write(bat_content)
