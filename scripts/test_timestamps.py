import os
import subprocess
import time

QA_OUT_DIR = r'C:\Projects\prasannakaragar\scripts\qa_renders'
CHROME_PATH = r'C:\Program Files\Google\Chrome\Application\chrome.exe'
ROOT_DIR = r'C:\Projects\prasannakaragar'

# SVGs are in ../../assets/ relative to scripts/qa_renders/
timestamps = [0, 2, 5, 9, 13]

for t in timestamps:
    test_html = f"""<!DOCTYPE html>
<html>
<head>
  <style>
    body {{ background: #070b16; margin: 0; padding: 20px; }}
    * {{
      animation-delay: -{t}s !important;
    }}
  </style>
</head>
<body>
  <div style="display:flex; flex-direction:column; gap:20px; max-width:850px; margin:0 auto;">
    <img src="../../assets/hero.svg?v=1" style="width:100%;">
    <img src="../../assets/about-life.svg?v=1" style="width:100%;">
    <img src="../../assets/stack.svg?v=1" style="width:100%;">
    <img src="../../assets/id-dashboard.svg?v=1" style="width:100%;">
    <img src="../../assets/connect.svg?v=1" style="width:100%;">
  </div>
</body>
</html>"""
    hpath = os.path.join(QA_OUT_DIR, f"harness_{t}s.html")
    with open(hpath, 'w', encoding='utf-8') as f:
        f.write(test_html)

    out_png = os.path.join(QA_OUT_DIR, f"render_{t}s.png")
    subprocess.run([
        CHROME_PATH,
        '--headless=new',
        '--disable-gpu',
        '--no-sandbox',
        '--allow-file-access-from-files',
        '--window-size=950,2200',
        f'--screenshot={out_png}',
        hpath
    ], capture_output=True)

    if os.path.exists(out_png):
        print(f"Rendered timestamp {t}s -> {os.path.basename(out_png)} ({os.path.getsize(out_png)} bytes)")

# Test with animation disabled (static render fallback)
test_static = """<!DOCTYPE html>
<html>
<head>
  <style>
    body { background: #070b16; margin: 0; padding: 20px; }
    * {
      animation: none !important;
      transition: none !important;
    }
  </style>
</head>
<body>
  <div style="display:flex; flex-direction:column; gap:20px; max-width:850px; margin:0 auto;">
    <img src="../../assets/hero.svg?v=1" style="width:100%;">
    <img src="../../assets/about-life.svg?v=1" style="width:100%;">
    <img src="../../assets/stack.svg?v=1" style="width:100%;">
    <img src="../../assets/id-dashboard.svg?v=1" style="width:100%;">
    <img src="../../assets/connect.svg?v=1" style="width:100%;">
  </div>
</body>
</html>"""

hpath_static = os.path.join(QA_OUT_DIR, "harness_static.html")
with open(hpath_static, 'w', encoding='utf-8') as f:
    f.write(test_static)

out_static = os.path.join(QA_OUT_DIR, "render_static.png")
subprocess.run([
    CHROME_PATH,
    '--headless=new',
    '--disable-gpu',
    '--no-sandbox',
    '--allow-file-access-from-files',
    '--window-size=950,2200',
    f'--screenshot={out_static}',
    hpath_static
], capture_output=True)

if os.path.exists(out_static):
    print(f"Rendered static fallback -> {os.path.basename(out_static)} ({os.path.getsize(out_static)} bytes)")

print("Timestamp render validation complete!")
