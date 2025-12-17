import os
try:
    from moviepy.editor import VideoFileClip
except ImportError as e:
    print(f"Warning: moviepy not available: {e}")
    VideoFileClip = None

def video_to_audio(video_file: str, audio_file: str = None):
    """Extract MP3 audio from a video file."""
    if not VideoFileClip:
        raise ImportError("moviepy library is not installed")
    
    if not audio_file:
        audio_file = os.path.splitext(video_file)[0] + ".mp3"
    
    try:
        video = VideoFileClip(video_file)
        video.audio.write_audiofile(audio_file)
        video.close()  # Important: close to free memory
        return audio_file
    except Exception as e:
        print(f"Error converting video to audio: {e}")
        raise

