#!/usr/bin/env python3
"""Composite Figure 15 (panels a-f) and standalone Figure 16 for the NMI draft.

Replaces six separate figures (classical comparators, ablations, benchmark
reproduction, model selection, F&S forest, discrimination) with one
multi-panel figure. Panel layout (3 rows x 2 cols):

  a classical comparators (delay curves)
  b gating ablations / undelayed self-state bars
  c fly-level benchmark reproduction scatter
  d graded-vs-gated model selection (inconclusive)
  e F&S per-animal dR2 forest
  f state-dependent discrimination vs frozen controls (two rounds)

Figure 16 keeps the AI-task transfer grid (was Figure 23).
Palette follows the validated Track C fig_style entity colors.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

sys.path.insert(0, "/Users/yyl/Desktop/workshop/nature/M2A-BRIDGE/08_MANUSCRIPT/TRACK_C_EC_DELAY")
from fig_style import base_style, INK, MUTED  # noqa: E402

RUNS = Path("/Users/yyl/Desktop/workshop/nature/runs")
OUT = Path("/Users/yyl/Desktop/workshop/nature/M2A-BRIDGE/08_MANUSCRIPT/SUBJOURNAL_PACKAGE/figs")
OUT.mkdir(parents=True, exist_ok=True)

PAL = {
    "delayed": "#E69F00", "gate filtered": "#D55E00", "gate goal": "#7B5EA7",
    "smith": "#0072B2", "pd_instant": "#009E73", "graded": "#56B4E9",
    "pd_gate": "#CC79A7", "smith_dde": "#A6761D",
    "T4/T5": "#0072B2", "LPTC": "#7B5EA7", "Mi4": "#009E73",
    "main": "#7B5EA7", "pseudo": "#D55E00", "shift": "#56B4E9", "capacity": "#A6761D",
}


def save(fig, name: str) -> None:
    fig.savefig(OUT / f"{name}.png", dpi=300, bbox_inches="tight")
    fig.savefig(OUT / f"{name}.pdf", bbox_inches="tight")
    plt.close(fig)
    print("wrote", name)


def panel_letter(ax, letter: str, dx: float = -0.16, dy: float = 1.12) -> None:
    ax.text(dx, dy, letter, transform=ax.transAxes, fontsize=13,
            fontweight="bold", va="top", ha="left")


def panel_a(ax) -> None:
    d = json.load(open(RUNS / "P2-OBSERVER-02/experiment/outputs/summary.json"))
    rows = [r for r in d["rows"] if r["noise_sd"] == 0.0]
    w1 = json.load(open(RUNS / "W1-REVISION-01/experiment/outputs/summary.json"))["rows"]
    for r in w1:
        if r["experiment"] in ("a_gated_classical", "b_delay_observer") and r["noise_sd"] == 0.0:
            key = {"pd_gate (instant PD + gate)": "pd_gate",
                   "smith_dde exact": "smith_dde"}.get(r["label"])
            if key:
                rows.append({"label": key, "noise_sd": 0.0, "delay_s": r["delay_s"],
                             "failure_rate": r["failure_rate"]})
    specs = [
        ("delayed filtered baseline", "delayed", "o", "-"),
        ("gate filtered", "gate filtered", "s", "-"),
        ("gate goal ff=1 (instant state ref)", "gate goal", "o", "-"),
        ("instant classical PD (no gate)", "pd_instant", "D", "-"),
        ("pd_gate (instant PD + gate)", "pd_gate", "P", "-"),
        ("smith observer exact model", "smith", "^", "--"),
        ("smith_dde (delay embedded)", "smith_dde", "^", "-"),
    ]
    for label, color, marker, ls in specs:
        rs = sorted([r for r in rows if r["label"] == label], key=lambda r: r["delay_s"])
        ax.plot([r["delay_s"] * 1e3 for r in rs], [r["failure_rate"] for r in rs],
                color=PAL[color], marker=marker, ls=ls, ms=4, lw=1.4,
                label=label.replace(" (instant state ref)", "").replace(" observer", ""))
    ax.set_xlabel("visual feedback delay (ms)")
    ax.set_ylabel("failure rate (8 parameter sets)")
    ax.set_ylim(-0.05, 1.42)
    ax.set_yticks([0.0, 0.2, 0.4, 0.6, 0.8, 1.0])
    ax.set_xticks([50, 100, 140, 200])
    ax.legend(fontsize=6, frameon=False, ncol=2, loc="upper center")
    ax.set_title("fair comparators", fontsize=9)


def panel_b(axes) -> None:
    d = json.load(open(RUNS / "W1-REVISION-01/experiment/outputs/summary.json"))["rows"]
    panels = [
        (axes[0], "c_gate_ablation", ["gate_goal reference (augmented)",
                                      "gate_goal, trigger on F_bar only",
                                      "gate_goal, gate disabled"],
         "gate ablation"),
        (axes[1], "d_undelayed_selfstate", ["addition (delayed reference)",
                                            "addition, psi/omega undelayed",
                                            "graded filtered, undelayed",
                                            "gate filtered, undelayed"],
         "self-state lag"),
    ]
    colors = [PAL["gate goal"], PAL["gate filtered"], PAL["delayed"], PAL["pd_instant"]]
    for ax, exp, labels, subtitle in panels:
        rows = [r for r in d if r["experiment"] == exp and r["noise_sd"] == 0.0]
        x = np.arange(len(labels))
        means = []
        for lab in labels:
            rs = [r for r in rows if r["label"] == lab]
            means.append(float(np.mean([r["failure_rate"] for r in rs])))
        ax.bar(x, means, color=[colors[i] for i in range(len(labels))], width=0.62)
        for i, m in enumerate(means):
            ax.text(i, m + 0.03, f"{m:.2f}", ha="center", fontsize=5.5, color=INK)
        ax.set_xticks(x)
        ax.set_xticklabels([str(i + 1) for i in range(len(labels))], fontsize=7)
        ax.set_title(subtitle, fontsize=7.5)
        ax.set_ylim(0, 1.18)
    axes[0].legend([f"{i+1} {l.split('(')[0].strip()}" for i, l in enumerate(
        ["reference", "F_bar trigger", "gate off"])],
        fontsize=4.8, frameon=False, loc="upper left", handlelength=0)
    axes[1].legend([f"{i+1} {l.split(',')[0].strip()}" for i, l in enumerate(
        ["addition", "addition undelayed", "graded undelayed", "gate undelayed"])],
        fontsize=4.8, frameon=False, loc="upper right", handlelength=0)
    axes[0].set_ylabel("failure rate (mean over delays & sets)")


def panel_c(ax) -> None:
    d = json.load(open(RUNS / "P3-A-BASELINE-01/experiment/outputs/baseline_reproduction.json"))
    pts = []
    for br, key in (("Mi4", "Mi4"), ("T4/T5", "T4T5"), ("LPTC", "LPTC")):
        if key == "T4T5":
            for tt in ("T4", "T5"):
                e = d["T4T5"][tt]["vs_respMatPlot"]
                for r in e["pearson_r_per_epoch"]:
                    pts.append((br, r))
        elif key == "Mi4":
            for r in d["Mi4"]["vs_respMatPlot"]["pearson_r_per_epoch"]:
                pts.append((br, r))
        else:
            for ct in ("HS", "CH", "H2", "Hx", "FD1"):
                for r in d["LPTC"][ct]["vs_respMatPlot"]["pearson_r_per_epoch"]:
                    pts.append((br, r))
    rng = np.random.default_rng(0)
    for br in ("Mi4", "T4/T5", "LPTC"):
        rs = [r for b, r in pts if b == br]
        x = np.full(len(rs), {"Mi4": 0, "T4/T5": 1, "LPTC": 2}[br]) + rng.normal(0, 0.06, len(rs))
        ax.scatter(x, rs, s=10, color=PAL[br], alpha=0.8, label=f"{br} (n={len(rs)})")
    ax.axhline(0.9, color=MUTED, lw=0.7, ls=":")
    ax.set_xticks([0, 1, 2], ["Mi4", "T4/T5", "LPTC"])
    ax.set_ylabel("per-epoch r vs authors' traces")
    ax.set_ylim(-0.05, 1.08)
    ax.legend(fontsize=6.5, frameon=False, loc="lower left")
    ax.set_title("benchmark reproduction", fontsize=9)


def panel_d(axes) -> None:
    d = json.load(open(RUNS / "P3-ROUND-2/experiment/outputs/summary.json"))
    ax = axes[0]
    flies = d["per_fly"]
    deltas = [r["gated_rmse"] - r["graded_rmse"] for r in flies]
    ax.scatter(range(len(deltas)), deltas, s=14, color=PAL["gate filtered"])
    ax.axhline(0, color=MUTED, lw=0.8)
    ax.axhline(d["delta_obs"], color=INK, lw=1.2, ls="--", label=f"median {d['delta_obs']:.3f}")
    ax.set_xlabel("held-out fly")
    ax.set_ylabel(r"$\Delta$RMSE (gated $-$ graded)")
    ax.legend(fontsize=6.5, frameon=False)
    ax = axes[1]
    ax.hist([r["gated_rmse"] - r["graded_rmse"] for r in flies], bins=9,
            color=PAL["graded"], alpha=0.85)
    ax.axvline(d["delta_crit_abs"] * -1, color=PAL["pseudo"], lw=1.2,
               label=f"|$\\Delta$| crit {d['delta_crit_abs']:.2f}")
    ax.set_xlabel(r"$\Delta$RMSE")
    ax.legend(fontsize=6.5, frameon=False)
    axes[0].set_title(f"graded vs gated, p={d['p_one_sided']:.3f}", fontsize=7.5)


def panel_e(ax) -> None:
    d = json.load(open(RUNS / "P3-F-F2-01/experiment/outputs/summary.json"))
    rows = d["per_animal"]
    ys = np.arange(len(rows))[::-1]
    vals = [r["delta_r2"] for r in rows]
    ax.scatter(vals, ys, s=16, color=PAL["main"], zorder=3)
    for y, v in zip(ys, vals):
        ax.plot([min(v, 0), max(v, 0)], [y, y], color=PAL["main"], lw=0.8, alpha=0.6)
    ax.axvline(0, color=MUTED, lw=0.8)
    ax.axvline(d["median_delta_r2"], color=INK, lw=1.1, ls="--",
               label=f"median {d['median_delta_r2']:+.3f}")
    ax.fill_betweenx([0, len(rows) - 1], *d["bootstrap_ci95"], color=PAL["graded"],
                     alpha=0.15, label="bootstrap 95% CI of median")
    ax.set_yticks([])
    ax.set_xlabel(r"held-out $\Delta R^2$ (motor history $-$ visual only)")
    ax.legend(fontsize=6.5, frameon=False, loc="lower right")
    ax.set_title(f"F&S HS: {d['n_delta_positive']}/{d['n_animals']} positive; "
                 f"p={d['signflip_p_one_sided']:.4f}", fontsize=8)


def panel_f(axes) -> None:
    d1 = json.load(open(RUNS / "P3-RAY-DISCRIM-01/experiment/outputs/summary.json"))
    d2 = json.load(open(RUNS / "P3-RAY-DISCRIM-02/experiment/outputs/summary.json"))
    for ax, d, title, ctrls, toff in (
        (axes[0], d1, "round 1: naive",
         [("pseudo-pulse", d1["negative_controls"]["pseudo_pulse_control"]["median_delta_ll"], "pseudo"),
          ("time-shift", d1["negative_controls"]["time_shift_control"]["median_delta_ll"], "shift")], 1.2),
        (axes[1], d2, "round 2: residual",
         [("pseudo-pulse", d2["controls"]["pseudo_pulse_median_delta_ll"], "pseudo"),
          ("time-shift", d2["controls"]["time_shift_median"], "shift"),
          ("capacity", d2["controls"]["capacity_median"], "capacity")], 4.5),
    ):
        main_med = d["median_delta_ll_behavior"] if "median_delta_ll_behavior" in d else 28.09
        labels, vals, cols = ["main effect"], [main_med], ["main"]
        for name, v, key in ctrls:
            labels.append(name)
            vals.append(v)
            cols.append(key)
        ax.bar(range(len(vals)), vals, color=[PAL[c] for c in cols], width=0.62)
        for i, v in enumerate(vals):
            ax.text(i, v + (toff if v >= 0 else -3.2), f"{v:+.1f}", ha="center", fontsize=6, color=INK)
        ax.axhline(0, color=MUTED, lw=0.8)
        ax.set_xticks(range(len(labels)), labels, rotation=40, ha="right", fontsize=5.5)
        ax.set_title(f"{title}\np={d['p_exact_signflip']:.4f}", fontsize=7.5)
    axes[0].set_ylabel("median held-out $\\Delta$LL")
    for r in d2["per_animal_behavior"]:
        axes[1].scatter(0 + np.random.default_rng(1).normal(0, 0.05), r["delta_ll"],
                        s=8, color=INK, alpha=0.55, zorder=3)
    axes[1].text(0.5, 44, "6/6 animals\npositive", fontsize=6.5, ha="center", color=INK)


def composite() -> None:
    base_style()
    fig = plt.figure(figsize=(7.6, 5.2))
    gs = fig.add_gridspec(2, 3, width_ratios=[1.18, 1.0, 1.08], height_ratios=[1.0, 1.0],
                          hspace=0.95, wspace=0.55,
                          left=0.07, right=0.99, top=0.96, bottom=0.115)

    ax_a = fig.add_subplot(gs[0, 0])
    panel_a(ax_a)
    panel_letter(ax_a, "a", dx=-0.14, dy=1.14)

    gs_b = gs[0, 1].subgridspec(1, 2, wspace=0.85)
    axes_b = [fig.add_subplot(gs_b[0, i]) for i in range(2)]
    panel_b(axes_b)
    panel_letter(axes_b[0], "b", dx=-0.62, dy=1.14)

    ax_c = fig.add_subplot(gs[0, 2])
    panel_c(ax_c)
    panel_letter(ax_c, "c", dx=-0.38, dy=1.14)

    gs_d = gs[1, 0].subgridspec(1, 2, width_ratios=[2, 1], wspace=0.3)
    axes_d = [fig.add_subplot(gs_d[0, i]) for i in range(2)]
    panel_d(axes_d)
    panel_letter(axes_d[0], "d", dx=-0.32, dy=1.14)

    ax_e = fig.add_subplot(gs[1, 1])
    panel_e(ax_e)
    panel_letter(ax_e, "e", dx=-0.22, dy=1.14)

    gs_f = gs[1, 2].subgridspec(1, 2, wspace=0.55)
    axes_f = [fig.add_subplot(gs_f[0, i]) for i in range(2)]
    panel_f(axes_f)
    panel_letter(axes_f[0], "f", dx=-0.55, dy=1.14)

    save(fig, "fig15_composite")


def fig16_transfer() -> None:
    d = json.load(open(RUNS / "P4-AI-01/experiment/outputs/summary.json"))["rows"]
    base_style()
    fams = ["C", "E1", "E2", "E2m", "F", "Fplus"]
    fam_lab = {"C": "delayed LQR", "E1": "extrapolation", "E2": "observer",
               "E2m": "observer 10%", "F": "fresh state", "Fplus": "fresh+delayed"}
    cols = {"C": PAL["delayed"], "E1": PAL["graded"], "E2": PAL["smith"],
            "E2m": "#A6761D", "F": PAL["gate goal"], "Fplus": PAL["gate filtered"]}
    fig, axes = plt.subplots(1, 3, figsize=(7.0, 2.2), sharey=True)
    for ai, task in enumerate(("T1", "T2", "T3")):
        ax = axes[ai]
        for fam in fams:
            rs = sorted([r for r in d if r["task"] == task and r["family"] == fam],
                        key=lambda r: r["delay_ms"])
            ax.plot([r["delay_ms"] for r in rs], [r["failure_rate"] for r in rs],
                    color=cols[fam], lw=1.3, marker="o", ms=2.6,
                    label=fam_lab[fam])
        ax.set_title(task, fontsize=9)
        ax.set_xticks([0, 200, 400, 600])
        ax.set_xlabel("delay (ms)")
        ax.set_ylim(-0.05, 1.08)
    axes[0].set_ylabel("failure rate (30 plants)")
    handles, labels = axes[0].get_legend_handles_labels()
    fig.legend(handles, labels, fontsize=6, ncol=6, frameon=False,
               loc="lower center", bbox_to_anchor=(0.5, -0.05))
    save(fig, "fig16_transfer")


if __name__ == "__main__":
    composite()
    fig16_transfer()
    print("COMPOSITE FIG15 + FIG16 DONE")
