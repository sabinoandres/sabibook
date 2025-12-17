import pytesseract
from PIL import Image

import os
import shutil

# Try to find Tesseract in common Windows locations if not in PATH
if not shutil.which("tesseract"):
    possible_paths = [
        r'C:\Program Files\Tesseract-OCR\tesseract.exe',
        r'C:\Program Files (x86)\Tesseract-OCR\tesseract.exe',
        os.path.expandvars(r'%LOCALAPPDATA%\Tesseract-OCR\tesseract.exe')
    ]
    for p in possible_paths:
        if os.path.exists(p):
            pytesseract.pytesseract.tesseract_cmd = p
            print(f"Detected Tesseract at: {p}")
            break

def image_to_text(file_path: str) -> str:
    """Extract text from image using OCR."""
    print(f"OCR: Processing file {file_path}")
    print(f"OCR: Using Tesseract CMD: {pytesseract.pytesseract.tesseract_cmd}")
    
    try:
        img = Image.open(file_path)
        text = pytesseract.image_to_string(img)
        print(f"OCR: Result length = {len(text)}")
        
        if not text.strip():
            return "Sabibook: No se detectó texto en la imagen. Intenta con una imagen más clara."
            
        return text
    except Exception as e:
        print(f"OCR Error: {e}")
        raise e

