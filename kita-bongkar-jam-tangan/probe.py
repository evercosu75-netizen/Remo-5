from playwright.sync_api import sync_playwright
with sync_playwright() as p:
    b = p.chromium.launch()
    pg = b.new_page(viewport={"width": 540, "height": 960})
    pg.goto("file:///home/hatch/workspace/kita-bongkar-jam-tangan/animatic.html")
    for t in (29.5, 30.0, 30.5, 20.0, 43.0):
        pg.evaluate(f"render({t})")
        print(t, "secRot=", pg.evaluate("document.getElementById('secRot').getAttribute('transform')"),
              "| balAng HUD=", pg.evaluate("document.getElementById('teleVal').textContent"),
              "| movOp=", pg.evaluate("document.getElementById('movementGroup').style.opacity"))
    b.close()
