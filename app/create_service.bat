call nssm.exe install itgrupo_printer_server "%cd%\run_server.bat"
call nssm.exe set itgrupo_printer_server AppStdout "%cd%\logs\itgrupo_printer_server_logs.log"
call nssm.exe set itgrupo_printer_server AppStderr "%cd%\logs\itgrupo_printer_server_logs.log"
call nssm set itgrupo_printer_server AppRotateFiles 1
call nssm set itgrupo_printer_server AppRotateOnline 1
call nssm set itgrupo_printer_server AppRotateSeconds 86400
call nssm set itgrupo_printer_server AppRotateBytes 1048576
call sc start itgrupo_printer_server