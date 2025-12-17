FROM python:3.10-slim

WORKDIR /app

# Install system dependencies
# ffmpeg for audio/video
# tesseract-ocr for OCR
# libreoffice for pdf conversion (linux alternative to word)
RUN apt-get update && apt-get install -y \
    ffmpeg \
    tesseract-ocr \
    libreoffice \
    default-jre \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
