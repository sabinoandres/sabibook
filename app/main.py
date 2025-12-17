from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
import shutil
import os
import secrets
# from app.services import audio, docs, image, video <-- Removed (Moving down)

# --- FFmpeg Fix ---
# --- FFmpeg Fix ---
# Whisper needs 'ffmpeg' command in PATH.
# We copy the binary from imageio-ffmpeg to a temp folder as 'ffmpeg.exe'
# Skip if already installed (e.g. in Docker via apt-get)
if not shutil.which("ffmpeg"):
    try:
        import imageio_ffmpeg as ffmpeg
        src_ffmpeg = ffmpeg.get_ffmpeg_exe()
        
        # Define our local bin folder
        local_bin = os.path.abspath("bin_tools")
        os.makedirs(local_bin, exist_ok=True)
        
        # Use .exe only on Windows
        ext = ".exe" if os.name == 'nt' else ""
        dst_ffmpeg = os.path.join(local_bin, f"ffmpeg{ext}")
        
        # Only copy if not exists to save time
        if not os.path.exists(dst_ffmpeg):
            print(f"Copying FFmpeg from {src_ffmpeg} to {dst_ffmpeg}...")
            shutil.copy2(src_ffmpeg, dst_ffmpeg)
        
        # Add to PATH
        os.environ["PATH"] += os.pathsep + local_bin
        
        # Explicitly tell tools where ffmpeg is
        os.environ["FFMPEG_BINARY"] = dst_ffmpeg
        os.environ["IMAGEIO_FFMPEG_EXE"] = dst_ffmpeg
        
        print(f"Correctly patched FFmpeg into PATH: {local_bin}")
    except ImportError:
        print("Warning: imageio_ffmpeg not found. Audio/Video conversions may fail.")
    except Exception as e:
        print(f"Error patching FFmpeg: {e}")
# ------------------
    
# (Handled above)
# ------------------

# Import services AFTER patching the environment
from app.services import audio, docs, image, video

app = FastAPI(title="Sabibook API")

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
    try:
        text = image.image_to_text(file_path)
        return {"text": text}
    except Exception as e:
        if "tesseract is not installed" in str(e).lower() or "not found" in str(e).lower():
             raise HTTPException(status_code=424, detail="Error: Tesseract-OCR no está instalado en el servidor. Consulta el README.")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/convert/video-to-audio")
async def video_audio_endpoint(file: UploadFile = File(...)):
    """Convert Video to Audio (MP3)."""
    file_path = save_upload_file(file)
    try:
        output_path = video.video_to_audio(file_path)
        return FileResponse(output_path, filename=os.path.basename(output_path))
    except Exception as e:
        print(f"Video conversion error: {e}") # Log to console
        raise HTTPException(status_code=500, detail=f"Error convert video: {str(e)}")

