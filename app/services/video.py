from moviepy.editor import VideoFileClip
import os

def video_to_audio(video_file: str, audio_file: str = None):
    """Extract MP3 audio from a video file."""
    if not audio_file:
        audio_file = os.path.splitext(video_file)[0] + ".mp3"
        
    video = VideoFileClip(video_file)
    video.audio.write_audiofile(audio_file)
    return audio_file

