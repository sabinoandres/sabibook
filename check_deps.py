import shutil
import sys

def check_tool(name):
    path = shutil.which(name)
    print(f"{name}: {'FOUND at ' + path if path else 'NOT FOUND'}")

print("Checking dependencies...")
check_tool("ffmpeg")
check_tool("tesseract")

try:
    import pytesseract
    print(f"Pytesseract tesseract_cmd: {pytesseract.pytesseract.tesseract_cmd}")
except:
    pass
