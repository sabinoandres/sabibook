# Sabibook API

Una potente API basada en Python para la conversión de medios y documentos.

## Funcionalidades
- **Audio a Texto**: Usa el modelo Whisper de OpenAI.
- **PDF a Word**: Usa `pdf2docx`.
- **Word a PDF**: Usa `docx2pdf` (Windows) o `libreoffice`.
- **OCR (Imagen a Texto)**: Usa `pytesseract` (Tesseract-OCR).
- **PDF a PowerPoint**: Extracción simple de texto a Diapositivas.
- **Video a Audio**: Usa `moviepy` (FFmpeg).

## Prerrequisitos
Debes instalar las siguientes herramientas del sistema y añadirlas a tu PATH:
1. **FFmpeg**: Para procesamiento de audio/video. [Descargar](https://ffmpeg.org/download.html)
2. **Tesseract-OCR**: Para extracción de texto de imágenes. [Descargar](https://github.com/UB-Mannheim/tesseract/wiki)
3. **Microsoft Word** (Windows) o **LibreOffice** (Linux/Mac) para conversión de Word->PDF.

## Configuración
1. Crea un entorno virtual:
   ```bash
   python -m venv venv
   source venv/bin/activate  # o venv\Scripts\activate en Windows
   ```
2. Instala las dependencias:
   ```bash
   pip install -r requirements.txt
   ```

## Ejecutar la API
```bash
uvicorn app.main:app --reload
```
Accede a la documentación de la API en: `http://localhost:8000/docs`

## Soporte Docker
También puedes ejecutarlo vía Docker (maneja las dependencias automáticamente):
```bash
docker build -t converter-app .
docker run -p 8000:8000 converter-app
```
