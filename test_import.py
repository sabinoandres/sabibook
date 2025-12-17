import sys
print("Python Executable:", sys.executable)
try:
    import fastapi
    print("FastAPI imported successfully from:", fastapi.__file__)
except ImportError as e:
    print("Error importing fastapi:", e)
except Exception as e:
    print("Other error:", e)
