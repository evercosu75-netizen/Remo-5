"""Render animatic per adegan lalu gabung. Batas adegan dibaca dari halaman (window.BOUNDS).
python3 render.py [narasi.mp3]"""
import sys, os, subprocess, pathlib
from playwright.sync_api import sync_playwright

here = pathlib.Path(__file__).parent.resolve()
parts = here / "parts"; parts.mkdir(exist_ok=True)
FPS = 30
NAME = os.environ.get("NAME", "video-explainer")
with sync_playwright() as p:
    b = p.chromium.launch()
    pg = b.new_page(viewport={"width": 540, "height": 960}, device_scale_factor=2)
    pg.goto((here / "animatic.html").as_uri())
    pg.evaluate("document.fonts.ready")
    BOUNDS = pg.evaluate("window.BOUNDS")
    print("BOUNDS", BOUNDS, flush=True)
    stage = pg.locator("#stage")
    for i in range(len(BOUNDS) - 1):
        n0, n1 = round(BOUNDS[i] * FPS), round(BOUNDS[i + 1] * FPS)
        tmp = parts / f"s{i+1}.tmp.mp4"
        ff = subprocess.Popen(["ffmpeg", "-loglevel", "error", "-y", "-f", "image2pipe", "-framerate", str(FPS), "-c:v", "mjpeg", "-i", "-",
               "-vf", "scale=1080:1920,format=yuv420p", "-c:v", "libx264", "-preset", "veryfast", "-crf", "19",
               "-pix_fmt", "yuv420p", "-r", str(FPS), str(tmp)], stdin=subprocess.PIPE)
        for n in range(n0, n1):
            pg.evaluate(f"render({n / FPS})")
            ff.stdin.write(stage.screenshot(type="jpeg", quality=92))
        ff.stdin.close()
        if ff.wait() != 0: sys.exit(f"adegan {i+1} gagal")
        os.replace(tmp, parts / f"s{i+1}.mp4"); print("adegan", i + 1, "ok", n1 - n0, "frame", flush=True)
    b.close()
lst = parts / "list.txt"
lst.write_text("".join(f"file 's{i+1}.mp4'\n" for i in range(len(BOUNDS) - 1)))
video = here / "video-only.mp4"
subprocess.run(["ffmpeg", "-loglevel", "error", "-y", "-f", "concat", "-safe", "0", "-i", str(lst), "-c", "copy", str(video)], check=True)
audio = sys.argv[1] if len(sys.argv) > 1 else None
out = here / (f"{NAME}-final.mp4" if audio else f"{NAME}-animatic.mp4")
if audio:
    subprocess.run(["ffmpeg", "-loglevel", "error", "-y", "-i", str(video), "-i", audio, "-map", "0:v", "-map", "1:a",
                    "-c:v", "copy", "-af", "apad", "-c:a", "aac", "-b:a", "192k", "-shortest", str(out)], check=True)
else:
    subprocess.run(["ffmpeg", "-loglevel", "error", "-y", "-i", str(video), "-f", "lavfi", "-i", "anullsrc=r=48000:cl=stereo",
                    "-map", "0:v", "-map", "1:a", "-c:v", "copy", "-c:a", "aac", "-shortest", str(out)], check=True)
print("selesai:", out)
