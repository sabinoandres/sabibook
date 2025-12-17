from pdf2docx import Converter
from docx2pdf import convert
import os
from pptx import Presentation
from pptx.util import Inches
import PyPDF2

def pdf_to_word(pdf_file: str, word_file: str = None):
    # ... (existing code) ...
    """Convert PDF to Word DOCX."""
    if not word_file:
        word_file = os.path.splitext(pdf_file)[0] + ".docx"
    
    cv = Converter(pdf_file)
    cv.convert(word_file, start=0, end=None)
    cv.close()
    return word_file

def word_to_pdf(word_file: str, pdf_file: str = None):
    # ... (existing code) ...
    """Convert Word DOCX to PDF (Windows using Word, Linux using LibreOffice)."""
    if not pdf_file:
        pdf_file = os.path.splitext(word_file)[0] + ".pdf"
    
    convert(word_file, pdf_file)
    return pdf_file

def pdf_to_ppt(pdf_file: str, ppt_file: str = None):
    """Convert PDF text to PowerPoint slides."""
    if not ppt_file:
        ppt_file = os.path.splitext(pdf_file)[0] + ".pptx"
        
    prs = Presentation()
    
    try:
        reader = PyPDF2.PdfReader(pdf_file)
        for page in reader.pages:
            text = page.extract_text()
            if text.strip():
                slide_layout = prs.slide_layouts[1] # Title and Content
                slide = prs.slides.add_slide(slide_layout)
                
                # Set title to generic page number or first line
                title = slide.shapes.title
                title.text = f"Page {reader.get_page_number(page) + 1}"
                
                content = slide.placeholders[1]
                content.text = text
                
        prs.save(ppt_file)
        return ppt_file
    except Exception as e:
        print(f"Error converting PDF to PPT: {e}")
        return None


