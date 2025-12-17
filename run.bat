@echo off
echo Iniciando el servidor...
echo Intenta acceder a http://localhost:8000 en tu navegador.
echo Presiona CTRL+C para detenerlo.
echo.

python -m uvicorn app.main:app --reload || py -m uvicorn app.main:app --reload || echo "Error: No se pudo encontrar Python. Asegurate de instalar Python y agregarlo al PATH." && pause
