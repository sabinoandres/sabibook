@echo off
echo ==========================================
echo    INSTALADOR Y LANZADOR DE DIAGNOSTICO
echo ==========================================
echo.
echo 1. Buscando Python...
where python
IF %ERRORLEVEL% NEQ 0 (
    echo [ERROR] No se encontro 'python'. 
    echo Por favor instala Python desde https://www.python.org/downloads/
    echo Y asegurate de marcar "Add Python to PATH" durante la instalacion.
    pause
    exit /b
)

echo.
echo 2. Instalando partes necesarias (esto puede tardar)...
python -m pip install -r requirements.txt
IF %ERRORLEVEL% NEQ 0 (
    echo [ERROR] Fallo la instalacion de librerias.
    echo Probando con 'py' launcher...
    py -m pip install -r requirements.txt
)

echo.
echo 3. Iniciando el servidor...
echo ------------------------------------------
echo VE A ESTA DIRECCION EN TU NAVEGADOR:
echo http://localhost:8000
echo ------------------------------------------
python -m uvicorn app.main:app --reload

echo.
echo [AVISO] El servidor se ha cerrado o ha fallado.
pause
