from pathlib import Path
import json, textwrap
from PIL import Image, ImageDraw, ImageFont
import sys

ROOT = Path.cwd()
JSON_FILE = ROOT / "reports" / "inference_output.json"
OUT = ROOT / "reports" / "inference_example.png"

def load_json_robust(path):
    b = path.read_bytes()
    # try common encodings
    for enc in ("utf-8", "utf-8-sig", "utf-16", "latin-1"):
        try:
            s = b.decode(enc)
            return json.loads(s)
        except Exception:
            pass
    # last resort: ignore errors and try
    try:
        s = b.decode("utf-8", errors="ignore")
        return json.loads(s)
    except Exception as e:
        raise RuntimeError(f"Cannot decode JSON file {path}: {e}")

def find_image():
    candidates = list((ROOT/"data"/"plant_disease").rglob("*.jpg")) + list((ROOT/"data"/"plant_disease").rglob("*.JPG")) \
               + list((ROOT/"data"/"plant_disease").rglob("*.jpeg")) + list((ROOT/"data"/"plant_disease").rglob("*.png"))
    if not candidates:
        raise FileNotFoundError("No images found under data/plant_disease. Adjust path or provide an image.")
    return candidates[0]

# load inference JSON robustly
try:
    data = load_json_robust(JSON_FILE)
except Exception as e:
    print("ERROR loading JSON:", e, file=sys.stderr)
    raise

img_path = find_image()
img = Image.open(img_path).convert("RGB")

# resize input image to max height 600, keep aspect ratio
max_h = 600
w, h = img.size
scale = min(1.0, max_h / h)
nw, nh = int(w*scale), int(h*scale)
img = img.resize((nw, nh))

# create right pane with white background and draw pretty JSON
pane_w = 800
pane_h = max(nh, max_h)
pane = Image.new("RGB", (pane_w, pane_h), "white")
draw = ImageDraw.Draw(pane)
try:
    font = ImageFont.truetype("arial.ttf", 14)
except Exception:
    font = ImageFont.load_default()

txt = json.dumps(data, indent=2, ensure_ascii=False)
lines = textwrap.wrap(txt, width=60)
y = 10
for line in lines:
    draw.text((10, y), line, fill="black", font=font)
    y += 16
    if y > pane_h - 20:
        break

# compose final image (left image + right text pane)
margin = 20
final_w = nw + pane_w + margin
final_h = max(nh, pane_h)
final = Image.new("RGB", (final_w, final_h), "white")
final.paste(img, (0, 0))
final.paste(pane, (nw + margin, 0))

OUT.parent.mkdir(parents=True, exist_ok=True)
final.save(OUT, quality=90)
print("Saved:", OUT)
