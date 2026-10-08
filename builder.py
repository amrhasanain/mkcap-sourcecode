import subprocess
import sys
import traceback

try:
    python = r"C:\Users\khali\AppData\Local\Programs\Python\Python314\python.exe"

    print("Starting Nuitka...\n")

    result = subprocess.run([
        python,
        "-m",
        "nuitka",
        "--onefile",
        "--remove-output",
        "mkcap.py"
    ])

    print("\nNuitka finished.")
    print("Exit code:", result.returncode)

except Exception:
    traceback.print_exc()

finally:
    input("\nPress Enter to exit...")