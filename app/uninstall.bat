@echo off
set "archivo_vbs=C:\Users\jrevi\AppData\Roaming\Microsoft\Windows\Start Menu\Programs\Startup\ocultar_script.vbs"
set "archivo_bat=C:\Users\jrevi\AppData\Roaming\Microsoft\Windows\Start Menu\Programs\Startup\run_project.bat"

if exist "%archivo_vbs%" (
    del "%archivo_vbs%"
)
if exist "%archivo_bat%" (
    del " %archivo_bat%"
)
pause
echo Presiona cualquier tecla para abrir terminar...