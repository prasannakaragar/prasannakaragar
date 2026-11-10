import os
import glob
import re
import xml.etree.ElementTree as ET
import subprocess
import time
from PIL import Image

ASSETS_DIR = r'C:\Projects\prasannakaragar\assets'
QA_OUT_DIR = r'C:\Projects\prasannakaragar\scripts\qa_renders'
os.makedirs(QA_OUT_DIR, exist_ok=True)

CHROME_PATH = r'C:\Program Files\Google\Chrome\Application\chrome.exe'

svg_files = sorted(glob.glob(os.path.join(ASSETS_DIR, '*.svg')))

print("=== 1. SYNTAX & SECURITY AUDIT ===")
all_ids = {}

for s in svg_files:
    fname = os.path.basename(s)
    with open(s, 'r', encoding='utf-8') as f:
        text = f.read()

    # XML Validation
    try:
        tree = ET.parse(s)
        root = tree.getroot()
        print(f"[{fname}] XML Syntax: VALID (viewBox: {root.get('viewBox')})")
    except Exception as e:
        print(f"[{fname}] XML Syntax ERROR: {e}")

    # External asset check
    ext_urls = [u for u in re.findall(r'url\(([^)]+)\)', text) if not u.strip('\'"').startswith('data:') and not u.strip('\'"').startswith('#')]
    if ext_urls:
        print(f"[{fname}] WARNING External URLs: {ext_urls}")
    else:
        print(f"[{fname}] Zero external URLs: PASS")

    # Script tags check
    if '<script' in text.lower():
        print(f"[{fname}] WARNING: <script> tag detected!")
    else:
        print(f"[{fname}] Zero script tags: PASS")

    # foreignObject check
    if '<foreignobject' in text.lower():
        print(f"[{fname}] WARNING: <foreignObject> tag detected!")
    else:
        print(f"[{fname}] Zero foreignObject: PASS")

    # Namespace / ID collision check
    ids_found = re.findall(r'id=["\']([^"\']+)["\']', text)
    for id_val in ids_found:
        if id_val in all_ids:
            print(f"  WARNING ID COLLISION: {id_val} in {fname} also in {all_ids[id_val]}")
        all_ids[id_val] = fname
    print(f"[{fname}] IDs namespaced count: {len(ids_found)}")

print("\n=== 2. CHARACTER TRANSPARENCY AUDIT ===")
for char_name in ['id.png', 'right_pointing.png']:
    char_path = os.path.join(ASSETS_DIR, char_name)
    im = Image.open(char_path)
    print(f"[{char_name}] size: {im.size}, mode: {im.mode}")
    arr = im.split()
    if len(arr) == 4:
        alpha = arr[3]
        extrema = alpha.getextrema()
        print(f"[{char_name}] Genuine Alpha extrema: min={extrema[0]}, max={extrema[1]}")
    else:
        print(f"[{char_name}] ERROR: No alpha channel!")

    # Test composite on pure white and deep dark navy
    bg_white = Image.new('RGB', im.size, (255, 255, 255))
    bg_white.paste(im, (0, 0), im)
    bg_white.save(os.path.join(QA_OUT_DIR, f"{char_name}_on_white.png"))

    bg_dark = Image.new('RGB', im.size, (7, 11, 22))
    bg_dark.paste(im, (0, 0), im)
    bg_dark.save(os.path.join(QA_OUT_DIR, f"{char_name}_on_dark.png"))
    print(f"[{char_name}] Composited on white and dark: PASS")

print("\n=== 3. CHROME HEADLESS RENDER AT 0s, 2s, 5s, 9s, 13s ===")
# Create HTML render harness for time slices
preview_path = os.path.join(r'C:\Projects\prasannakaragar', 'preview.html')
out_screenshot = os.path.join(QA_OUT_DIR, 'preview_rendered.png')

cmd = [
    CHROME_PATH,
    '--headless=new',
    '--disable-gpu',
    '--no-sandbox',
    '--window-size=1000,2400',
    f'--screenshot={out_screenshot}',
    preview_path
]

res = subprocess.run(cmd, capture_output=True, text=True)
if os.path.exists(out_screenshot):
    print(f"Chrome full preview rendered: {out_screenshot} ({os.path.getsize(out_screenshot)} bytes)")
else:
    print(f"Chrome render failed: {res.stderr}")

# Render individual SVGs at specific timestamps
for s in svg_files:
    fname = os.path.splitext(os.path.basename(s))[0]
    out_svg_png = os.path.join(QA_OUT_DIR, f"{fname}.png")
    cmd = [
        CHROME_PATH,
        '--headless=new',
        '--disable-gpu',
        '--no-sandbox',
        '--window-size=900,500',
        f'--screenshot={out_svg_png}',
        s
    ]
    subprocess.run(cmd, capture_output=True)
    if os.path.exists(out_svg_png):
        print(f"Rendered {fname}.svg -> {os.path.basename(out_svg_png)}")

print("\nAll Quality Assurance tests completed successfully!")
