FROM python:3.10-slim

WORKDIR /app

# Install system dependencies
# ffmpeg for audio/video
# tesseract-ocr for OCR
# (LibreOffice removed: Too heavy for 512MB Render Free Tier)
RUN apt-get update && apt-get install -y --no-install-recommends \
    ffmpeg \
    tesseract-ocr \
    && rm -rf /var/lib/apt/lists/*

# Install Torch CPU-only FIRST (Critical for memory/space)
RUN pip install --no-cache-dir torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cpu

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
