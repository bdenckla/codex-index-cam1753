"""Download pages 77-90 from Cambridge Ms. Add. 1753 on archive.org."""
import os
from urllib.request import urlopen, Request

OUT_DIR = os.path.join(os.path.dirname(__file__), "cam1753-spreads")
os.makedirs(OUT_DIR, exist_ok=True)

BASE_URL = (
    "https://ia800901.us.archive.org/BookReader/BookReaderImages.php"
    "?zip=/28/items/ketuvim-cambridge-ms-add-1753-images"
    "/Ketuvim_Cambridge_MS_Add_1753_jp2.zip"
    "&file=Ketuvim_Cambridge_MS_Add_1753_jp2"
    "/Ketuvim_Cambridge_MS_Add_1753_{page:04d}.jp2"
    "&id=ketuvim-cambridge-ms-add-1753-images"
    "&scale=2&rotate=0"
)

for page in range(77, 91):
    url = BASE_URL.format(page=page)
    out_path = os.path.join(OUT_DIR, f"cam1753-page-{page:04d}.jpg")
    if os.path.exists(out_path):
        print(f"  Already exists: {out_path}")
        continue
    print(f"  Downloading page {page} ...")
    req = Request(url, headers={"User-Agent": "Mozilla/5.0"})
    with urlopen(req, timeout=60) as resp:
        data = resp.read()
    with open(out_path, "wb") as f:
        f.write(data)
    print(f"    Saved {len(data)} bytes -> {out_path}")

print("Done.")
