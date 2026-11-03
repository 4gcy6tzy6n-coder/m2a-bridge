#!/usr/bin/env python3
"""Build a single contact sheet of the 16 completed manuscript figures.

Source: the exact PNGs embedded in latex_nmi/manuscript.tex (Fig. 1-16).
Output: figures_contact_sheet.png / .pdf

Layout: two columns of fixed width; each row is as tall as its tallest
panel, so no panel is letter-boxed and no title overlaps a neighbour.
No data is redrawn and no figure pixels are altered apart from uniform
scaling.
"""

from __future__ import annotations

from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.image as mpimg
import matplotlib.pyplot as plt

HERE = Path(__file__).resolve().parent
IMG_DIR = HERE.parent / "latex_nmi" / "figs"  # final set embedded in manuscript.tex
OUT = HERE

# (figure number, file stem, short title) in manuscript order
FIGS = [
    (1, "fig1_model", "Model and delay manipulation"),
    (2, "fig2c_gain_delay_heatmap", "Efference-copy gain by delay"),
    (3, "fig_window_check", "Window dependence of the gating comparison"),
    (4, "fig_stress", "V-term and gate-threshold stress tests"),
    (5, "fig_adaptive_gradient", "Adaptive updates"),
    (6, "fig_command_copy", "Command copy vs filtered plant state"),
    (7, "fig_feedforward", "Goal feedforward and its mechanism controls"),
    (8, "fig_mechanism", "Mechanism summary"),
    (9, "fig_delay_limits", "Delay limits"),
    (10, "fig_noise", "Noise robustness"),
    (11, "fig_trajectories", "Example trajectories at 200 ms"),
    (12, "fig_survival", "Failure-free curves at 140 ms"),
    (13, "fig_phase", "Body-parameter phase diagram"),
    (14, "fig_selfstate", "Freshness, timing and content of the self-state signal"),
    (15, "fig15_composite", "Fair comparators, ablations, empirical constraints"),
    (16, "fig16_transfer", "Freshness hierarchy transfers to artificial tasks"),
]

PAGE_W = 23.0          # inches
MARGIN = 0.45
COL_GAP = 0.55
TITLE_H = 0.34         # inches reserved above each panel
ROW_GAP = 0.42
HEADER_H = 0.85
FOOTER_H = 0.35
COLS = 2

INK = "#101010"
MUTED = "#5F5F5F"
ACCENT = "#7B5EA7"

col_w = (PAGE_W - 2 * MARGIN - (COLS - 1) * COL_GAP) / COLS

# pre-measure panels: displayed height keeps native aspect ratio
panels = []
for num, stem, title in FIGS:
    img = mpimg.imread(IMG_DIR / f"{stem}.png")
    h, w = img.shape[:2]
    panels.append({"num": num, "title": title, "img": img, "h_disp": col_w * h / w})

rows = [panels[i:i + COLS] for i in range(0, len(panels), COLS)]
row_heights = [max(p["h_disp"] for p in r) for r in rows]
page_h = HEADER_H + sum(h + TITLE_H for h in row_heights) + ROW_GAP * (len(rows) - 1) + FOOTER_H

fig = plt.figure(figsize=(PAGE_W, page_h), facecolor="white")

fig.text(MARGIN / PAGE_W, 1 - 0.34 / page_h,
         "Completed figure set — Nature Machine Intelligence submission draft",
         fontsize=19, color=INK, weight="bold", ha="left", va="center")
fig.text(MARGIN / PAGE_W, 1 - 0.62 / page_h,
         "16 figures; PNG masters 220–300 dpi with vector PDFs alongside",
         fontsize=11, color=MUTED, ha="left", va="center")

y = HEADER_H
for row, row_h in zip(rows, row_heights):
    for j, p in enumerate(row):
        x = MARGIN + j * (col_w + COL_GAP)
        # title sits inside the reserved strip, above the image
        fig.text(x / PAGE_W, 1 - (y + TITLE_H * 0.62) / page_h,
                 f"Fig. {p['num']}  ·  {p['title']}",
                 fontsize=12.5, color=INK, weight="bold", ha="left", va="center")
        fig.text((x + col_w) / PAGE_W, 1 - (y + TITLE_H * 0.62) / page_h,
                 f"{p['img'].shape[1]}×{p['img'].shape[0]} px",
                 fontsize=8.5, color=MUTED, ha="right", va="center")

        top = y + TITLE_H
        ax = fig.add_axes([x / PAGE_W, 1 - (top + p["h_disp"]) / page_h,
                           col_w / PAGE_W, p["h_disp"] / page_h])
        ax.imshow(p["img"], interpolation="lanczos")
        ax.set_xticks([]); ax.set_yticks([])
        for spine in ax.spines.values():
            spine.set_visible(False)
    y += row_h + TITLE_H + ROW_GAP

fig.text(MARGIN / PAGE_W, FOOTER_H * 0.55 / page_h,
         "Source: SUBJOURNAL_PACKAGE/latex_nmi/figs/*.png exactly as embedded in manuscript.tex "
         "(\\\\includegraphics order). No data redrawn; panels scaled proportionally only.",
         fontsize=9, color=MUTED, ha="left", va="center")

fig.savefig(OUT / "figures_contact_sheet.png", dpi=200, facecolor="white")
fig.savefig(OUT / "figures_contact_sheet.pdf", facecolor="white")
print(f"wrote figures_contact_sheet.png/.pdf  page={PAGE_W:.1f}x{page_h:.1f} in")
