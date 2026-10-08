import shutil
import subprocess
import sys
import json
from pathlib import Path
from rich.console import Console  # type: ignore[import-not-found]

console = Console()

def fail(msg):
    console.print(f"[bold red]❌ Error:[/bold red] {msg}")
    sys.exit(1)

def find_tool(name):
    exe = name + (".exe" if sys.platform.startswith("win") else "")
    for base in (Path(__file__).resolve().parent.parent.parent, Path.cwd()):
        for p in (base / "ffmpeg" / exe, base / exe):
            if p.exists():
                return str(p)
    found = shutil.which(name)
    if not found:
        fail(f"{name} not found. Install FFmpeg or put it in ./ffmpeg/")
    return found

def run(cmd, cwd=None):
    r = subprocess.run(cmd, capture_output=True, text=True, cwd=cwd)
    if r.returncode != 0:
        console.print("[red]" + "\n".join(r.stderr.strip().splitlines()[-8:]) + "[/red]")
        fail("FFmpeg execution failed.")
    return r

def video_size(ffprobe, path):
    try:
        out = subprocess.check_output([
            ffprobe, "-v", "error", "-select_streams", "v:0",
            "-show_streams", "-of", "json", str(path)],
            text=True, stderr=subprocess.DEVNULL)
        st = json.loads(out)["streams"][0]
        w, h = int(st["width"]), int(st["height"])
        rot = st.get("tags", {}).get("rotate")
        if rot is None:
            rot = next((d["rotation"] for d in st.get("side_data_list", []) if "rotation" in d), 0)
        return (h, w) if abs(int(float(rot))) in (90, 270) else (w, h)
    except Exception:
        return 1920, 1080