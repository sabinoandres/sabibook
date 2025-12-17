import whisper
import gc
import torch

# Global placeholder
_model = None

def get_model():
    """Lazy load the model only when needed."""
    global _model
    if _model is None:
        # Use 'tiny' model for low memory environments (Render free tier)
        _model = whisper.load_model("tiny")
    return _model

def transcribe_audio(file_path: str) -> str:
    """Transcribe audio to text using OpenAI Whisper."""
    try:
        model = get_model()
        result = model.transcribe(file_path)
        return result["text"]
    except Exception as e:
        print(f"Error during transcription: {e}")
        return str(e)
    finally:
        # Optional: Aggressive memory cleanup if 512MB is strictly enforced
        # global _model
        # _model = None
        # gc.collect()
        # torch.cuda.empty_cache() if torch.cuda.is_available() else None
        pass


