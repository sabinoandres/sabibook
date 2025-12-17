try:
    from moviepy import VideoFileClip
    print("MoviePy imported successfully!")
except ImportError as e:
    print("Error importing MoviePy:", e)
    # Fallback check for v1.0 path
    try:
        from moviepy.editor import VideoFileClip
        print("Wait, moviepy.editor works? Then version is < 2.0")
    except ImportError:
        print("moviepy.editor also failed")
