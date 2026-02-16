"""
Generate an interactive HTML editor for adjusting column/line
locations on an Aleppo Codex page image.

Shows the full page image with a transparent overlay of two columns,
each containing 28 red line segments. The user can drag control
points to adjust column positions and line spacing.

Usage:
    python py_ac_loc/gen_col_location_editor.py 270r
"""

import sys
import webbrowser
from pathlib import Path

BASE = Path(__file__).resolve().parent.parent
OUT_DIR = BASE / ".novc"

LINES_PER_COL = 28


def _leaf_to_page_n(page_id):
    """Convert a leaf ID like '270r' to the archive.org 0-based page index."""
    num = int(page_id[:-1])
    side = page_id[-1]
    return (num - 1) * 2 + 2 + (0 if side == "r" else 1)


def _image_url(page_id):
    """Build archive.org direct image URL for an Aleppo Codex page."""
    n = _leaf_to_page_n(page_id)
    return (
        "https://ia601801.us.archive.org/BookReader/BookReaderImages.php"
        f"?zip=/7/items/aleppo-codex/Aleppo%20Codex_jp2.zip"
        f"&file=Aleppo%20Codex_jp2/Aleppo%20Codex_{n:04d}.jp2"
        f"&id=aleppo-codex&scale=2&rotate=0"
    )


def generate_editor(page_id):
    """Generate the HTML column-location editor for a page."""

    img_url = _image_url(page_id)

    html = f"""\
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<title>Column Location Editor \u2014 {{page_id}}</title>
<style>
  * {{ margin: 0; padding: 0; box-sizing: border-box; }}
  body {{
    background: #222;
    color: #eee;
    font-family: system-ui, sans-serif;
    overflow: hidden;
  }}
  #toolbar {{
    position: fixed;
    top: 0; left: 0; right: 0;
    height: 36px;
    background: #333;
    display: flex;
    align-items: center;
    padding: 0 12px;
    gap: 12px;
    z-index: 100;
    font-size: 14px;
  }}
  #toolbar button {{
    padding: 4px 12px;
    cursor: pointer;
    border: 1px solid #666;
    background: #444;
    color: #eee;
    border-radius: 3px;
  }}
  #toolbar button:hover {{ background: #555; }}
  #toolbar .info {{ color: #aaa; margin-left: auto; }}
  #container {{
    position: absolute;
    top: 36px; left: 0; right: 0; bottom: 0;
    overflow: auto;
    display: flex;
    justify-content: center;
  }}
  #page-wrapper {{
    position: relative;
    display: inline-block;
  }}
  #page-wrapper img {{
    display: block;
    height: calc(100vh - 36px);
    width: auto;
  }}
  #overlay {{
    position: absolute;
    top: 0; left: 0; right: 0; bottom: 0;
    pointer-events: none;
  }}
  #overlay svg {{
    width: 100%;
    height: 100%;
  }}
  /* Control points are interactive */
  .ctrl-point {{
    pointer-events: all;
    cursor: grab;
    fill: rgba(0, 200, 255, 0.6);
    stroke: #0af;
    stroke-width: 1;
  }}
  .ctrl-point:hover {{
    fill: rgba(0, 200, 255, 0.9);
  }}
  .ctrl-point.dragging {{
    cursor: grabbing;
    fill: #ff0;
  }}
</style>
</head>
<body>

<div id="toolbar">
  <span><b>Col Location</b> \u2014 {page_id}</span>
  <button id="fine-btn" onclick="toggleFine()">Fine: OFF</button>
  <button onclick="rotate(-1)">Rotate \u21B6</button>
  <button onclick="rotate(+1)">Rotate \u21B7</button>
  <button onclick="resetPositions()">Reset</button>
  <button onclick="exportJSON()">Export JSON</button>
  <span class="info" id="status">Drag side handles to resize; buttons to rotate</span>
</div>

<div id="container">
  <div id="page-wrapper">
    <img id="page-img" src="{img_url}" alt="Codex page {page_id}">
    <div id="overlay">
      <svg id="overlay-svg" viewBox="0 0 1000 1000" preserveAspectRatio="none">
      </svg>
    </div>
  </div>
</div>

<script>
const LINES = {LINES_PER_COL};
const DEG = Math.PI / 180;

// Each column is a rectangle: centre (cx,cy), half-extents (hw,hh), angle in degrees.
// Col 1 = right column, Col 2 = left column.
const DEFAULTS = {{
  col1: {{ cx: 0.7358, cy: 0.4547, hw: 0.1897, hh: 0.3659, angle: 0 }},
  col2: {{ cx: 0.27,   cy: 0.4561, hw: 0.19,   hh: 0.3667, angle: 0 }},
}};

let cols = JSON.parse(JSON.stringify(DEFAULTS));

const svg = document.getElementById('overlay-svg');
const status = document.getElementById('status');

// Fine mode: scale down mouse deltas by FINE_SCALE for precise adjustments.
let fineMode = false;
const FINE_SCALE = 0.2;  // 1/5 sensitivity

function toggleFine() {{
  fineMode = !fineMode;
  document.getElementById('fine-btn').textContent = fineMode ? 'Fine: ON' : 'Fine: OFF';
  document.getElementById('fine-btn').style.background = fineMode ? '#070' : '';
}}

// --- Geometry helpers ---

function corners(r) {{
  // Returns {{ tl, tr, bl, br }} in normalised coords, applying rotation.
  const cos = Math.cos(r.angle * DEG);
  const sin = Math.sin(r.angle * DEG);
  function pt(dx, dy) {{
    return {{ x: r.cx + dx * cos - dy * sin, y: r.cy + dx * sin + dy * cos }};
  }}
  return {{
    tl: pt(-r.hw, -r.hh),
    tr: pt(+r.hw, -r.hh),
    bl: pt(-r.hw, +r.hh),
    br: pt(+r.hw, +r.hh),
  }};
}}

function midpoints(r) {{
  // Returns {{ top, bottom, left, right }} midpoints of each side.
  const cos = Math.cos(r.angle * DEG);
  const sin = Math.sin(r.angle * DEG);
  function pt(dx, dy) {{
    return {{ x: r.cx + dx * cos - dy * sin, y: r.cy + dx * sin + dy * cos }};
  }}
  return {{
    top:    pt(0, -r.hh),
    bottom: pt(0, +r.hh),
    left:   pt(-r.hw, 0),
    right:  pt(+r.hw, 0),
  }};
}}

function lerp(a, b, t) {{
  return {{ x: a.x + (b.x - a.x) * t, y: a.y + (b.y - a.y) * t }};
}}

function clamp(v) {{ return Math.max(0, Math.min(1, v)); }}

// --- Drawing ---

function drawAll() {{
  while (svg.firstChild) svg.removeChild(svg.firstChild);

  for (const [colName, r] of Object.entries(cols)) {{
    const colNum = colName === 'col1' ? 1 : 2;
    const colour = colNum === 1 ? 'rgba(255, 60, 60, 0.7)' : 'rgba(60, 120, 255, 0.7)';
    const handleColour = colNum === 1 ? 'rgba(255, 80, 80, 0.8)' : 'rgba(80, 140, 255, 0.8)';
    const c = corners(r);

    // Draw line segments.
    for (let i = 0; i < LINES; i++) {{
      const t = LINES === 1 ? 0.5 : i / (LINES - 1);
      const left = lerp(c.tl, c.bl, t);
      const right = lerp(c.tr, c.br, t);

      const line = document.createElementNS('http://www.w3.org/2000/svg', 'line');
      line.setAttribute('x1', left.x * 1000);
      line.setAttribute('y1', left.y * 1000);
      line.setAttribute('x2', right.x * 1000);
      line.setAttribute('y2', right.y * 1000);
      line.setAttribute('stroke', colour);
      line.setAttribute('stroke-width', '1.5');
      svg.appendChild(line);

      const mid = lerp(left, right, 0.5);
      const label = document.createElementNS('http://www.w3.org/2000/svg', 'text');
      label.setAttribute('x', mid.x * 1000);
      label.setAttribute('y', mid.y * 1000 - 3);
      label.setAttribute('text-anchor', 'middle');
      label.setAttribute('font-size', '8');
      label.setAttribute('fill', colour);
      label.textContent = `${{colNum}}:${{i + 1}}`;
      svg.appendChild(label);
    }}

    // Side-midpoint handles (each adjusts only one dimension).
    const m = midpoints(r);
    for (const side of ['top', 'bottom', 'left', 'right']) {{
      const pt = m[side];
      const circle = document.createElementNS('http://www.w3.org/2000/svg', 'circle');
      circle.setAttribute('cx', pt.x * 1000);
      circle.setAttribute('cy', pt.y * 1000);
      circle.setAttribute('r', '8');
      circle.setAttribute('class', 'ctrl-point');
      circle.setAttribute('fill', handleColour);
      circle.setAttribute('stroke', handleColour);
      circle.setAttribute('data-col', colName);
      circle.setAttribute('data-side', side);
      svg.appendChild(circle);
    }}

    // Bounding rectangle outline.
    const outline = document.createElementNS('http://www.w3.org/2000/svg', 'polygon');
    const pts = [c.tl, c.tr, c.br, c.bl]
      .map(p => `${{p.x * 1000}},${{p.y * 1000}}`)
      .join(' ');
    outline.setAttribute('points', pts);
    outline.setAttribute('fill', 'none');
    outline.setAttribute('stroke', colour);
    outline.setAttribute('stroke-width', '1');
    outline.setAttribute('stroke-dasharray', '6 3');
    svg.appendChild(outline);
  }}
}}

// --- Dragging (side handles, each adjusts only one dimension) ---

let dragTarget = null;
let dragCol = null;
let dragSide = null;
let dragStartMouse = null;   // mouse pos at drag start (normalised)
let dragStartRect = null;    // snapshot of rect params at drag start

svg.addEventListener('mousedown', (e) => {{
  if (e.target.classList.contains('ctrl-point')) {{
    dragTarget = e.target;
    dragCol = dragTarget.getAttribute('data-col');
    dragSide = dragTarget.getAttribute('data-side');
    dragTarget.classList.add('dragging');
    const svgRect = svg.getBoundingClientRect();
    dragStartMouse = {{
      x: (e.clientX - svgRect.left) / svgRect.width,
      y: (e.clientY - svgRect.top) / svgRect.height,
    }};
    dragStartRect = JSON.parse(JSON.stringify(cols[dragCol]));
    e.preventDefault();
  }}
}});

window.addEventListener('mousemove', (e) => {{
  if (!dragTarget) return;
  const svgRect = svg.getBoundingClientRect();
  let mx = (e.clientX - svgRect.left) / svgRect.width;
  let my = (e.clientY - svgRect.top) / svgRect.height;

  // In fine mode, scale the delta from the drag-start position.
  if (fineMode) {{
    mx = dragStartMouse.x + (mx - dragStartMouse.x) * FINE_SCALE;
    my = dragStartMouse.y + (my - dragStartMouse.y) * FINE_SCALE;
  }}
  mx = clamp(mx);
  my = clamp(my);

  // Reset rect to drag-start state, then apply new position.
  const r0 = dragStartRect;
  const r = cols[dragCol];
  r.cx = r0.cx; r.cy = r0.cy; r.hw = r0.hw; r.hh = r0.hh;

  const cos = Math.cos(r.angle * DEG);
  const sin = Math.sin(r.angle * DEG);

  // Vector from centre to mouse, projected onto rotated local axes.
  const dx = mx - r.cx;
  const dy = my - r.cy;
  const localX = dx * cos + dy * sin;
  const localY = -dx * sin + dy * cos;

  // Each side handle moves the corresponding edge while keeping
  // the opposite edge fixed (adjusting cx/cy + hw or hh).
  if (dragSide === 'right') {{
    // localX = new hw; shift centre so left edge stays put.
    const newHw = Math.max(0.01, localX);
    const shift = (newHw - r.hw) / 2;
    r.cx += shift * cos;
    r.cy += shift * sin;
    r.hw = newHw;
  }} else if (dragSide === 'left') {{
    const newHw = Math.max(0.01, -localX);
    const shift = (newHw - r.hw) / 2;
    r.cx -= shift * cos;
    r.cy -= shift * sin;
    r.hw = newHw;
  }} else if (dragSide === 'bottom') {{
    const newHh = Math.max(0.01, localY);
    const shift = (newHh - r.hh) / 2;
    r.cx -= shift * sin;
    r.cy += shift * cos;
    r.hh = newHh;
  }} else if (dragSide === 'top') {{
    const newHh = Math.max(0.01, -localY);
    const shift = (newHh - r.hh) / 2;
    r.cx += shift * sin;
    r.cy -= shift * cos;
    r.hh = newHh;
  }}

  drawAll();
  updateStatus();
}});

window.addEventListener('mouseup', () => {{
  if (dragTarget) {{
    dragTarget.classList.remove('dragging');
    dragTarget = null;
  }}
}});

// --- Rotation ---

function rotate(degrees) {{
  const d = fineMode ? degrees * FINE_SCALE : degrees;
  cols.col1.angle += d;
  cols.col2.angle += d;
  drawAll();
  updateStatus();
}}

// --- Status ---

function updateStatus() {{
  const c1 = corners(cols.col1);
  const c2 = corners(cols.col2);
  const a = cols.col1.angle.toFixed(1);
  status.textContent =
    `Angle: ${{a}}\u00b0  |  ` +
    `Col 1: TL(${{f(c1.tl)}}) BR(${{f(c1.br)}})  |  ` +
    `Col 2: TL(${{f(c2.tl)}}) BR(${{f(c2.br)}})`;
}}

function f(pt) {{ return `${{(pt.x * 100).toFixed(1)}}%,${{(pt.y * 100).toFixed(1)}}%`; }}

// --- Reset ---

function resetPositions() {{
  cols = JSON.parse(JSON.stringify(DEFAULTS));
  drawAll();
  updateStatus();
}}

// --- Export ---

function exportJSON() {{
  const img = document.getElementById('page-img');
  const W = img.naturalWidth;
  const H = img.naturalHeight;

  function pxPt(pt) {{ return {{ x: Math.round(pt.x * W), y: Math.round(pt.y * H) }}; }}

  const result = {{}};
  for (const [colName, r] of Object.entries(cols)) {{
    const colNum = colName === 'col1' ? 1 : 2;
    const c = corners(r);
    const linesRel = [];
    const linesPx = [];
    for (let i = 0; i < LINES; i++) {{
      const t = LINES === 1 ? 0.5 : i / (LINES - 1);
      const left = lerp(c.tl, c.bl, t);
      const right = lerp(c.tr, c.br, t);
      linesRel.push({{
        line: i + 1,
        left: {{ x: round4(left.x), y: round4(left.y) }},
        right: {{ x: round4(right.x), y: round4(right.y) }},
      }});
      linesPx.push({{
        line: i + 1,
        left: pxPt(left),
        right: pxPt(right),
      }});
    }}
    result[`col${{colNum}}`] = {{
      rect: {{
        cx: round4(r.cx), cy: round4(r.cy),
        hw: round4(r.hw), hh: round4(r.hh),
        angle: round4(r.angle),
      }},
      corners_rel: {{
        tl: {{ x: round4(c.tl.x), y: round4(c.tl.y) }},
        tr: {{ x: round4(c.tr.x), y: round4(c.tr.y) }},
        bl: {{ x: round4(c.bl.x), y: round4(c.bl.y) }},
        br: {{ x: round4(c.br.x), y: round4(c.br.y) }},
      }},
      corners_px: {{
        tl: pxPt(c.tl), tr: pxPt(c.tr),
        bl: pxPt(c.bl), br: pxPt(c.br),
      }},
      lines_rel: linesRel,
      lines_px: linesPx,
    }};
  }}
  const json = JSON.stringify({{
    page: "{page_id}",
    image_size: {{ width: W, height: H }},
    columns: result,
  }}, null, 2);
  navigator.clipboard.writeText(json).then(() => {{
    status.textContent = 'JSON copied to clipboard!';
    setTimeout(updateStatus, 2000);
  }});
}}

function round4(v) {{ return Math.round(v * 10000) / 10000; }}

// --- Init ---

drawAll();
updateStatus();
</script>
</body>
</html>
"""

    OUT_DIR.mkdir(exist_ok=True)
    out_path = OUT_DIR / f"col_editor_{page_id}.html"
    out_path.write_text(html, encoding="utf-8")
    print(f"Editor written to {out_path}")
    webbrowser.open(out_path.as_uri())


def main():
    if len(sys.argv) < 2:
        print("Usage: python py_ac_loc/gen_col_location_editor.py <page_id>")
        print("  e.g. python py_ac_loc/gen_col_location_editor.py 270r")
        sys.exit(1)
    page_id = sys.argv[1]
    generate_editor(page_id)


if __name__ == "__main__":
    main()
