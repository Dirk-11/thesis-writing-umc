"""
generate_workflow.py — Recreate workflow_v3_3.png with updated labels:
  - 414 stones (was 421)
  - Model A: Weighted CE loss (was CE loss)
  - Model B: Weighted KL + BCE loss (was KL + BCE loss)
"""
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import FancyBboxPatch
from pathlib import Path

OUT = Path(__file__).parent / "figures" / "workflow_v3_3.png"

# ── Colours ───────────────────────────────────────────────────────────────────
C_DATASET   = ("#B8D4E8", "#5A8FC0")   # fill, edge
C_PREP      = ("#C8E6C8", "#5A9C5A")
C_A         = ("#F5C0C0", "#C04040")
C_B         = ("#D8C8F0", "#7040C0")
C_C         = ("#F5C0D8", "#C04070")
C_METRIC_A  = ("#FADADC", "#C04040")
C_METRIC_B  = ("#E8DCFC", "#7040C0")
C_METRIC_C  = ("#FCD8EC", "#C04070")
C_COMPARE   = ("#FAE0B0", "#C08040")
C_ARROW     = "#666666"
C_TEXT      = "#222222"


def rounded_box(ax, cx, cy, w, h, lines, fill, edge,
                fontsize=9, bold_first=True, radius=0.015):
    """Draw a rounded-rect box centred at (cx,cy) with one or more text lines."""
    patch = FancyBboxPatch(
        (cx - w / 2, cy - h / 2), w, h,
        boxstyle=f"round,pad=0,rounding_size={radius}",
        linewidth=1.3, edgecolor=edge, facecolor=fill, zorder=3,
        transform=ax.transData,
    )
    ax.add_patch(patch)
    if isinstance(lines, str):
        lines = [lines]
    n = len(lines)
    spacing = h / (n + 1)
    for i, line in enumerate(lines):
        y = cy + h / 2 - spacing * (i + 1)
        fw = "bold" if (bold_first and i == 0) else "normal"
        ax.text(cx, y, line, ha="center", va="center",
                fontsize=fontsize, fontweight=fw, color=C_TEXT,
                fontfamily="DejaVu Sans", zorder=4)


def arr(ax, x0, y0, x1, y1):
    ax.annotate("", xy=(x1, y1), xytext=(x0, y0),
                arrowprops=dict(arrowstyle="-|>", color=C_ARROW,
                                lw=1.3, mutation_scale=13),
                zorder=2)


def main():
    fig, ax = plt.subplots(figsize=(7.5, 7.0))
    ax.set_xlim(0, 1)
    ax.set_ylim(0.24, 1.0)
    ax.axis("off")
    fig.patch.set_facecolor("white")

    # ── MOCKI dataset ────────────────────────────────────────────────────────
    rounded_box(ax, 0.50, 0.920, 0.52, 0.085,
                ["MOCKI dataset",
                 "414 stones × 3 photos + FTIR labels"],
                *C_DATASET, fontsize=9.5)
    arr(ax, 0.50, 0.877, 0.50, 0.822)

    # ── Preprocessing ────────────────────────────────────────────────────────
    rounded_box(ax, 0.50, 0.790, 0.68, 0.080,
                ["Preprocessing",
                 "Data cleaning · OTH remapping · 9→5 classes",
                 "Composition vectors (Σ=1)"],
                *C_PREP, fontsize=8.5)

    # ResNet18 annotation (italic, small)
    ax.text(0.50, 0.740, "ResNet18 · ImageNet pretrained · staged fine-tuning",
            ha="center", va="center", fontsize=8, color="#555555",
            fontfamily="DejaVu Sans", style="italic", zorder=4)

    # Trunk down to branch point
    arr(ax, 0.50, 0.750, 0.50, 0.700)

    # ── Branch arrows to three models ────────────────────────────────────────
    branch_y = 0.700
    # Horizontal line
    ax.plot([0.17, 0.83], [branch_y, branch_y], color=C_ARROW, lw=1.3, zorder=2)
    # Down to each model
    for x in [0.17, 0.50, 0.83]:
        arr(ax, x, branch_y, x, 0.650)

    # ── Model boxes ──────────────────────────────────────────────────────────
    model_y  = 0.605
    model_h  = 0.090
    model_w  = 0.28

    rounded_box(ax, 0.17, model_y, model_w, model_h,
                ["Model A", "Binary classifier", "Weighted CE loss"],
                *C_A, fontsize=8.5)

    rounded_box(ax, 0.50, model_y, model_w, model_h,
                ["Model B", "Compositional regression", "Weighted KL + BCE loss"],
                *C_B, fontsize=8.5)

    rounded_box(ax, 0.83, model_y, model_w, model_h,
                ["Model C", "Multiclass classifier", "Weighted CE loss"],
                *C_C, fontsize=8.5)

    # ── Arrows to metric boxes ────────────────────────────────────────────────
    metric_y = 0.465
    for x in [0.17, 0.50, 0.83]:
        arr(ax, x, model_y - model_h / 2, x, metric_y + 0.040)

    # ── Metric boxes ─────────────────────────────────────────────────────────
    metric_h = 0.055
    metric_w = 0.26

    rounded_box(ax, 0.17, metric_y, metric_w, metric_h,
                ["AUC-ROC, F1"], *C_METRIC_A, fontsize=8.5, bold_first=False)

    rounded_box(ax, 0.50, metric_y, metric_w, metric_h,
                ["MAE, dominant F1"], *C_METRIC_B, fontsize=8.5, bold_first=False)

    rounded_box(ax, 0.83, metric_y, metric_w, metric_h,
                ["Macro F1, per-class F1"], *C_METRIC_C, fontsize=8.5, bold_first=False)

    # ── Arrows to comparison boxes ────────────────────────────────────────────
    compare_y = 0.320
    # Model A → Threshold comparison
    arr(ax, 0.17, metric_y - metric_h / 2, 0.17, compare_y + 0.048)
    # Model B + C → Dominant class comparison
    for x in [0.50, 0.83]:
        ax.plot([x, x], [metric_y - metric_h / 2, compare_y + 0.048],
                color=C_ARROW, lw=1.3, zorder=2)
    ax.plot([0.50, 0.83], [compare_y + 0.048, compare_y + 0.048],
            color=C_ARROW, lw=1.3, zorder=2)
    arr(ax, 0.665, compare_y + 0.048, 0.665, compare_y + 0.045)

    # ── Comparison boxes ──────────────────────────────────────────────────────
    cmp_h = 0.072
    cmp_w = 0.30

    rounded_box(ax, 0.17, compare_y, cmp_w, cmp_h,
                ["Threshold comparison", "90% vs 100% purity"],
                *C_COMPARE, fontsize=8.5)

    rounded_box(ax, 0.665, compare_y, 0.36, cmp_h,
                ["Dominant class comparison", "Model B dominant vs Model C"],
                *C_COMPARE, fontsize=8.5)

    plt.tight_layout(pad=0.2)
    fig.savefig(OUT, dpi=150, bbox_inches="tight")
    plt.close(fig)
    print(f"Saved: {OUT}")


if __name__ == "__main__":
    main()
