@echo off

rem Leer el archivo requirements.txt línea por línea
for /F %%i in (requirements.txt) do (
    pip show %%i > nul
    if errorlevel 1 (
        echo %%i no está instalado. Instalando...
        pip install %%i
    )
)

rem Ejecuta el programa principal
python main.py