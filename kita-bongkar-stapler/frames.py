"""Ambil frame kunci animatic untuk diperiksa: python3 frames.py 4.5 15 ..."""
import sys, pathlib
from playwright.sync_api import sync_playwright

here = pathlib.Path(__file__).parent.resolve()
out = here / "cek"
out.mkdir(exist_ok=True)
times = [float(x) for x in sys.argv[1:]]
with sync_playwright() as p:
    b = p.chromium.launch()
    pg = b.new_page(viewport={"width": 540, "height": 960}, device_scale_factor=2)
    pg.goto((here / "animatic.html").as_uri())
    pg.evaluate("document.fonts.ready")
    for t in times:
        pg.evaluate(f"render({t})")
        pg.locator("#stage").screenshot(path=str(out / f"t{t:05.1f}.jpg"), type="jpeg", quality=85)
    b.close()
print("ok", len(times))
