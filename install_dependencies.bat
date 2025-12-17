@echo off
echo Installing Python dependencies...

REM Upgrade pip first
python -m pip install --upgrade pip

REM Install requirements
pip install -r requirements.txt

REM Install additional system dependencies if needed
echo.
echo Installation complete!
echo.
echo Note: For full functionality, you may also need:
echo - FFmpeg (for video processing)
echo - Tesseract OCR (for image text extraction)
echo.
pause