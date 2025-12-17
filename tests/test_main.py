from fastapi.testclient import TestClient
from unittest.mock import patch, MagicMock
from app.main import app

client = TestClient(app)

def test_read_main():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Welcome to the All-in-One Converter API"}

@patch("app.services.audio.transcribe_audio")
def test_transcribe_endpoint(mock_transcribe):
    # Mock the return value
    mock_transcribe.return_value = "Hello World"
    
    # Create a dummy file
    files = {"file": ("test.mp3", b"fake audio content", "audio/mpeg")}
    
    response = client.post("/transcribe", files=files)
    
    assert response.status_code == 200
    assert response.json() == {"text": "Hello World"}
    mock_transcribe.assert_called_once()

@patch("app.services.image.image_to_text")
def test_ocr_endpoint(mock_ocr):
    mock_ocr.return_value = "Extracted Text"
    files = {"file": ("image.png", b"fake image content", "image/png")}
    
    response = client.post("/ocr", files=files)
    
    assert response.status_code == 200
    assert response.json() == {"text": "Extracted Text"}
    mock_ocr.assert_called_once()

@patch("app.services.docs.pdf_to_ppt")
def test_pdf_to_ppt_endpoint(mock_ppt):
    # Mock returning a path to a fake file
    mock_ppt.return_value = "temp_files/test.pptx"
    
    # We need to create the fake file so FileResponse can read it
    import os
    os.makedirs("temp_files", exist_ok=True)
    with open("temp_files/test.pptx", "wb") as f:
        f.write(b"fake ppt content")

    files = {"file": ("doc.pdf", b"fake pdf content", "application/pdf")}
    
    response = client.post("/convert/pdf-to-ppt", files=files)
    
    assert response.status_code == 200
    # Cleanup
    if os.path.exists("temp_files/test.pptx"):
        os.remove("temp_files/test.pptx")
