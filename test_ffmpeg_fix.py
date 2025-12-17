import os
import imageio_ffmpeg as ffmpeg
import shutil

print(f"Original PATH includes ffmpeg? {'ffmpeg' in os.environ['PATH']}")

ffmpeg_path = os.path.dirname(ffmpeg.get_ffmpeg_exe())
os.environ["PATH"] += os.pathsep + ffmpeg_path

print(f"Injected PATH: {ffmpeg_path}")

if shutil.which("ffmpeg"):
    print("SUCCESS: ffmpeg found in PATH after injection!")
else:
    print("FAILURE: ffmpeg still not found.")
