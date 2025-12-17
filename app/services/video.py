from moviepy import VideoFileClip
import os

def video_to_audio(video_file: str, audio_file: str = None):
    """Extract MP3 audio from a video file."""
    if not audio_file:
        audio_file = os.path.splitext(video_file)[0] + ".mp3"
        
    video = VideoFileClip(video_file)
    
    if video.audio is None:
        video.close()
        raise ValueError("No audio track found in this video file (or FFmpeg failed to read it).")
        
    try:
        video.audio.write_audiofile(audio_file)
    finally:
        video.close()
        
    return audio_file

