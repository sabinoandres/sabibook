import pytesseract
from PIL import Image

# Ensure tesseract is in path or configure it here
# pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

def image_to_text(file_path: str) -> str:
    """Extract text from image using OCR."""
    img = Image.open(file_path)
    text = pytesseract.image_to_string(img)
    return text

