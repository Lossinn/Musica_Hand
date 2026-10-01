"""Convierte SVG/HTML a PNG o PDF con Microsoft Edge (headless)."""
import subprocess, sys, tempfile
from pathlib import Path
EDGE = r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"

def png(src: Path, out: Path, w: int, h: int, scale: float = 1.0, transparent=False):
    args = [EDGE, "--headless=new", "--disable-gpu", "--hide-scrollbars", f"--window-size={w},{h}",
            f"--force-device-scale-factor={scale}", f"--screenshot={out}"]
    if transparent: args.append("--default-background-color=00000000")
    args.append(src.resolve().as_uri())
    subprocess.run(args, check=True, capture_output=True, timeout=180)

def pdf(src: Path, out: Path):
    subprocess.run([EDGE, "--headless=new", "--disable-gpu", "--no-pdf-header-footer",
                    f"--print-to-pdf={out}", src.resolve().as_uri()], check=True, capture_output=True, timeout=300)

if __name__ == "__main__":
    src, out, w, h = Path(sys.argv[1]), Path(sys.argv[2]), int(sys.argv[3]), int(sys.argv[4])
    png(src, out, w, h, float(sys.argv[5]) if len(sys.argv) > 5 else 1.0)
