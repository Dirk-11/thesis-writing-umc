"""
generate_remapping.py — Two-panel class remapping figure for MOCKI dataset.
Left panel:  OTH subtype remapping to target classes.
Right panel: Full raw FTIR class → consolidated target class merging.
"""
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch
from pathlib import Path

OUT = Path(__file__).parent / "figures" / "class_remapping.png"

COLORS = {
    "CaOx": "#2166AC",
    "CaP":  "#D6604D",
    "UA":   "#4DAF4A",
    "MAP":  "#FF7F00",
    "CYS":  "#984EA3",
    "OTH":  "#888888",
}


def rounded_box(ax, cx, cy, w, h, main, sub="", color="#888888", fs=8.5):
    patch = FancyBboxPatch(
        (cx - w / 2, cy - h / 2), w, h,
        boxstyle="round,pad=0,rounding_size=0.018",
        linewidth=1.3, edgecolor=color,
        facecolor=color + "18", zorder=3, clip_on=False,
    )
    ax.add_patch(patch)
    if sub:
        ax.text(cx, cy + 0.014, main, ha="center", va="center",
                fontsize=fs, fontweight="bold", color="#1a1a1a", zorder=5, clip_on=False)
        ax.text(cx, cy - 0.019, sub, ha="center", va="center",
                fontsize=6.5, color="#555555", zorder=5, clip_on=False)
    else:
        ax.text(cx, cy, main, ha="center", va="center",
                fontsize=fs, fontweight="bold", color="#1a1a1a", zorder=5, clip_on=False)


def arr(ax, x0, y0, x1, y1, color, lw=1.0):
    ax.annotate(
        "", xy=(x1, y1), xytext=(x0, y0),
        arrowprops=dict(arrowstyle="-|>", color=color, lw=lw, mutation_scale=8),
        zorder=2, clip_on=False,
    )


def italic(ax, x, y, text, color, fs=6.5):
    ax.text(x, y, text, ha="center", va="center", fontsize=fs,
            color=color, style="italic", zorder=5, clip_on=False,
            bbox=dict(boxstyle="round,pad=0.08", facecolor="white",
                      edgecolor="none", alpha=0.75))


# ── Canvas ────────────────────────────────────────────────────────────────────
fig = plt.figure(figsize=(14, 6.8))
fig.patch.set_facecolor("white")

ax1 = fig.add_axes([0.01, 0.10, 0.39, 0.84])   # left  panel
ax2 = fig.add_axes([0.43, 0.10, 0.56, 0.84])   # right panel
for ax in (ax1, ax2):
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.axis("off")


# ══════════════════════════════════════════════════════════════════════════════
# LEFT PANEL — OTH subtype remapping
# ══════════════════════════════════════════════════════════════════════════════
ax1.text(0.50, 0.975, "OTH subtype remapping to target classes",
         ha="center", va="top", fontsize=10, fontweight="bold",
         color="#1a1a1a", transform=ax1.transAxes)
ax1.text(0.10, 0.935, "FTIR sub-identification", ha="left", va="top",
         fontsize=7.5, color="#666666", transform=ax1.transAxes)
ax1.text(0.78, 0.935, "Target class", ha="left", va="top",
         fontsize=7.5, color="#666666", transform=ax1.transAxes)

LX, RX = 0.30, 0.815
BW_L, BW_R = 0.52, 0.34
BH = 0.072

# Sub-type boxes
subtypes = [
    ("Na-H-urate hydrate (19)", 0.855, "UA"),
    ("Monoammonium urate (7)",  0.765, "UA"),
    ("Uric acid dihydrate (4)", 0.675, "UA"),
    ("Ca-Mg phosphate (4)",     0.510, "CaP"),
    ("Newberyite (1)",          0.390, "MAP"),
    ("Calcite (15)",            0.240, "OTH"),
    ("Protein / albumin (12)",  0.150, "OTH"),
    ("Xanthine (7)",            0.060, "OTH"),
]
for label, y, dest in subtypes:
    rounded_box(ax1, LX, y, BW_L, BH, label, color=COLORS[dest], fs=8)

# Target boxes
tgt_left = [
    ("UA",  "Uric acid",          0.765),
    ("CaP", "Calcium phosphate",  0.510),
    ("MAP", "Struvite",           0.390),
    ("OTH", "Remains OTH",       0.150),
]
for name, sub, y in tgt_left:
    rounded_box(ax1, RX, y, BW_R, 0.115, name, sub, color=COLORS[name], fs=9)

# Arrows + labels (UA group)
ua_y_tgt = 0.765
for src_y, lbl, lbl_dy in [
    (0.855, "urate salt",  +0.03),
    (0.765, "urate salt",   0.00),
    (0.675, "UA variant",  -0.03),
]:
    arr(ax1, LX + BW_L / 2, src_y, RX - BW_R / 2, ua_y_tgt, COLORS["UA"])
    mx = (LX + BW_L / 2 + RX - BW_R / 2) / 2
    my = (src_y + ua_y_tgt) / 2 + lbl_dy
    italic(ax1, mx, my, lbl, COLORS["UA"])

# CaP arrow
arr(ax1, LX + BW_L / 2, 0.510, RX - BW_R / 2, 0.510, COLORS["CaP"])
italic(ax1, (LX + BW_L / 2 + RX - BW_R / 2) / 2, 0.510 + 0.018, "phosphate", COLORS["CaP"])

# MAP arrow
arr(ax1, LX + BW_L / 2, 0.390, RX - BW_R / 2, 0.390, COLORS["MAP"])
italic(ax1, (LX + BW_L / 2 + RX - BW_R / 2) / 2, 0.390 + 0.018, "Mg phosphate", COLORS["MAP"])

# OTH arrows
oth_y_tgt = 0.150
for src_y, lbl, lbl_dy in [
    (0.240, "CaCO₃, not phosphate", +0.028),
    (0.150, "non-mineral",               0.000),
    (0.060, "purine, rare",             -0.028),
]:
    arr(ax1, LX + BW_L / 2, src_y, RX - BW_R / 2, oth_y_tgt, COLORS["OTH"])
    mx = (LX + BW_L / 2 + RX - BW_R / 2) / 2
    my = (src_y + oth_y_tgt) / 2 + lbl_dy
    italic(ax1, mx, my, lbl, COLORS["OTH"])

# Side brackets (left of sub-type boxes)
bx0, bx1 = 0.025, 0.045
for y_top, y_bot in [(0.895, 0.630), (0.280, 0.020)]:
    ax1.plot([bx0, bx1, bx1, bx0], [y_top, y_top, y_bot, y_bot],
             color="#aaaaaa", lw=0.9, clip_on=False)

# Summary strip
ax1.text(0.50, 0.025,
         "30 stones → UA   |   4 stones → CaP   |   1 stone → MAP   |   34 remain OTH",
         ha="center", va="center", fontsize=7.5, color="#333333",
         transform=ax1.transAxes,
         bbox=dict(boxstyle="round,pad=0.4", facecolor="#f5f5f5",
                   edgecolor="#cccccc", lw=0.8))


# ══════════════════════════════════════════════════════════════════════════════
# RIGHT PANEL — Full class merging
# ══════════════════════════════════════════════════════════════════════════════
ax2.text(0.50, 0.985, "Mineral class merging to target classes",
         ha="center", va="top", fontsize=10, fontweight="bold",
         color="#1a1a1a", transform=ax2.transAxes)
ax2.text(0.50, 0.950, "414 stones · 1242 images · 9 original → 6 target classes",
         ha="center", va="top", fontsize=7.5, color="#666666",
         transform=ax2.transAxes)
ax2.text(0.07, 0.915, "FTIR original class", ha="left", va="top",
         fontsize=7.5, color="#666666", transform=ax2.transAxes)
ax2.text(0.78, 0.915, "Target class", ha="left", va="top",
         fontsize=7.5, color="#666666", transform=ax2.transAxes)

LX2, RX2 = 0.22, 0.815
BW2L, BW2R = 0.36, 0.33

# Fixed y positions (data coords 0–1), leaving room for header above 0.87
raw = [
    ("COM (190)",  0.840, "CaOx"),
    ("COD (9)",    0.735, "CaOx"),
    ("CHP (90)",   0.605, "CaP"),
    ("CHPD (25)", 0.500, "CaP"),
    ("CMP (2)",   0.395, "CaP"),
    ("UA (36)",   0.285, "UA"),
    ("MAP (11)",  0.185, "MAP"),
    ("CYS (39)", 0.090, "CYS"),
    ("OTH (4)",   0.000, "OTH"),
]
shift = 0.0  # positions already absolute

for label, y, dest in raw:
    rounded_box(ax2, LX2, y, BW2L, 0.075, label, color=COLORS[dest], fs=8)

# Target classes
targets = [
    ("CaOx", "Calcium oxalate",   0.790),
    ("CaP",  "Calcium phosphate",  0.500),
    ("UA",   "Uric acid",          0.285),
    ("MAP",  "Struvite",           0.185),
    ("CYS",  "Cystine",            0.090),
    ("OTH",  "Excluded (B & C)",   0.000),
]
targets = [(n, s, y + shift) for n, s, y in targets]

for name, sub, y in targets:
    rounded_box(ax2, RX2, y, BW2R, 0.090, name, sub, color=COLORS[name], fs=9)

# Build lookup
raw_y   = {n.split(" (")[0]: y for n, y, c in raw}
tgt_y   = {n: y for n, s, y in targets}

# Arrow definitions: (raw_key, target, label, label_dy)
arrows = [
    ("COM",  "CaOx", "calcium oxalate",  +0.025),
    ("COD",  "CaOx", "calcium oxalate",  -0.025),
    ("CHP",  "CaP",  "hydroxyapatite",   +0.030),
    ("CHPD", "CaP",  "brushite",          0.000),
    ("CMP",  "CaP",  "whitlockite",      -0.030),
    ("UA",   "UA",   "",                  0.000),
    ("MAP",  "MAP",  "",                  0.000),
    ("CYS",  "CYS",  "",                  0.000),
    ("OTH",  "OTH",  "",                  0.000),
]

# For multi-source targets, spread landing points along the target box edge
# CaOx: COM lands top-right, COD lands bottom-right
# CaP: CHP top, CHPD mid, CMP bottom
tgt_land_offsets = {
    ("COM",  "CaOx"): +0.020,
    ("COD",  "CaOx"): -0.020,
    ("CHP",  "CaP"):  +0.025,
    ("CHPD", "CaP"):   0.000,
    ("CMP",  "CaP"):  -0.025,
}

for raw_key, tgt_key, lbl, lbl_dy in arrows:
    color = COLORS[tgt_key]
    y0 = raw_y[raw_key]
    y1 = tgt_y[tgt_key] + tgt_land_offsets.get((raw_key, tgt_key), 0)
    arr(ax2, LX2 + BW2L / 2, y0, RX2 - BW2R / 2, y1, color)
    if lbl:
        mx = (LX2 + BW2L / 2 + RX2 - BW2R / 2) / 2
        my = (y0 + y1) / 2 + lbl_dy
        italic(ax2, mx, my, lbl, color)

# OTH footnote
ax2.text(0.50, 0.022,
         "OTH (4): remaining after sub-identification reclassified 30 → UA · 4 → CaP · 1 → MAP; excluded from Models B & C",
         ha="center", va="center", fontsize=7, color="#666666",
         transform=ax2.transAxes)

# ── Save ──────────────────────────────────────────────────────────────────────
fig.savefig(OUT, dpi=160, bbox_inches="tight", facecolor="white")
plt.close(fig)
print(f"Saved: {OUT}")
