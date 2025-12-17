from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
import shutil
import os
import secrets

# Import services with error handling
try:
    from app.services import audio, docs, image, video
except ImportError as e:
    print(f"Warning: Some services may not be available: {e}")
    # Create dummy modules to prevent crashes
    class DummyService:
        def __getattr__(self, name):
            def dummy_func(*args, **kwargs):
                raise HTTPException(status_code=503, detail=f"Service not available: {name}")
            return dummy_func
    
    try:
        from app.services import audio
    except ImportError:
        audio = DummyService()
    
    try:
        from app.services import docs
    except ImportError:
        docs = DummyService()
    
    try:
        from app.services import image
    except ImportError:
        image = DummyService()
    
    try:
        from app.services import video
    except ImportError:
        video = DummyService()

app = FastAPI(title="All-in-One Converter API")

# Mount static files
app.mount("/static", StaticFiles(directory="app/static"), name="static")

TEMP_DIR = "temp_files"
os.makedirs(TEMP_DIR, exist_ok=True)

# ... (Helper function restored)
def save_upload_file(upload_file: UploadFile) -> str:
    """Helper to save uploaded file to temp dir."""
    file_path = os.path.join(TEMP_DIR, upload_file.filename or f"temp_{secrets.token_hex(4)}")
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(upload_file.file, buffer)
    return file_path


@app.get("/")
def read_root():
    """Serve the Web UI."""
    return FileResponse('app/static/index.html')


@app.post("/transcribe")
async def transcribe(file: UploadFile = File(...)):
    """Convert Audio to Text."""
    file_path = save_upload_file(file)
    try:
        text = audio.transcribe_audio(file_path)
        return {"text": text}
    finally:
        pass # Keep file for debugging or cleanup

@app.post("/convert/pdf-to-word")
async def pdf_to_doc(file: UploadFile = File(...)):
    """Convert PDF to Word."""
    file_path = save_upload_file(file)
    output_path = docs.pdf_to_word(file_path)
    return FileResponse(output_path, filename=os.path.basename(output_path))

@app.post("/convert/word-to-pdf")
async def doc_to_pdf_endpoint(file: UploadFile = File(...)):
    """Convert Word to PDF."""
    file_path = save_upload_file(file)
    output_path = docs.word_to_pdf(file_path)
    return FileResponse(output_path, filename=os.path.basename(output_path))

@app.post("/convert/pdf-to-ppt")
async def pdf_to_ppt_endpoint(file: UploadFile = File(...)):
    """Convert PDF to PowerPoint."""
    file_path = save_upload_file(file)
    output_path = docs.pdf_to_ppt(file_path)
    if not output_path:
        raise HTTPException(status_code=500, detail="Conversion failed")
    return FileResponse(output_path, filename=os.path.basename(output_path))

@app.post("/ocr")
async def ocr_endpoint(file: UploadFile = File(...)):
    """Extract text from Image."""
    file_path = save_upload_file(file)
    text = image.image_to_text(file_path)
    return {"text": text}

@app.post("/convert/video-to-audio")
async def video_audio_endpoint(file: UploadFile = File(...)):
    """Convert Video to Audio (MP3)."""
    file_path = save_upload_file(file)
    output_path = video.video_to_audio(file_path)
    return FileResponse(output_path, filename=os.path.basename(output_path))

