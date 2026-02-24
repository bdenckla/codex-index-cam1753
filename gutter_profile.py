"""Visualize column intensity profiles for cam1753 page spreads.

For each image, sum grayscale pixel values along each vertical column
(i.e. collapse the y-axis) to produce a 1-D brightness profile across
the width. Plot all profiles on one chart so we can see where the gutter
falls and how consistent it is across images.
"""

import os
import numpy as np
from PIL import Image
import matplotlib.pyplot as plt

IMG_DIR = "cam1753-spreads"
files = sorted(f for f in os.listdir(IMG_DIR) if f.endswith(".jpg"))

fig, axes = plt.subplots(len(files), 1, figsize=(14, 2.2 * len(files)), sharex=False)

for ax, fname in zip(axes, files):
    img = Image.open(os.path.join(IMG_DIR, fname)).convert("L")
    arr = np.array(img, dtype=np.float64)
    profile = arr.mean(axis=0)  # mean brightness per column
    w = arr.shape[1]
    ax.plot(range(w), profile, linewidth=0.5)
    ax.axvline(x=w // 2, color="red", linestyle="--", linewidth=0.8, label="midpoint")
    # mark the darkest column in the central 20%
    lo = int(w * 0.4)
    hi = int(w * 0.6)
    gutter_x = lo + np.argmin(profile[lo:hi])
    ax.axvline(
        x=gutter_x,
        color="green",
        linestyle="--",
        linewidth=0.8,
        label=f"min@{gutter_x}",
    )
    ax.set_ylabel(
        fname.replace("cam1753-page-", "").replace(".jpg", ""),
        fontsize=8,
        rotation=0,
        labelpad=40,
    )
    ax.set_xlim(0, max(4700, w))
    ax.tick_params(labelsize=7)
    ax.legend(fontsize=7, loc="upper right")

fig.suptitle(
    "Column-mean brightness profiles (grayscale)\n"
    "Red = image midpoint, Green = darkest column in central 20%",
    fontsize=11,
)
fig.tight_layout()
out = "cam1753-gutter-profiles.png"
fig.savefig(out, dpi=120)
print(f"Saved to {out}")
