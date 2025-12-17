try:
    import pytesseract
    from PIL import Image
except ImportError as e:
    print(f"Warning: OCR libraries not available: {e}")
    pytesseract = None
    Image = None

# Ensure tesseract is in path or configure it here
# pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

def image_to_text(file_path: str) -> str:
    """Extract text from image using OCR."""
    if not pytesseract or not Image:
        raise ImportError("pytesseract or PIL library is not installed")
    
    try:
        img = Image.open(file_path)
        text = pytesseract.image_to_string(img)
        return text
    except Exception as e:
        print(f"Error during OCR: {e}")
        return f"Error: {str(e)}"

