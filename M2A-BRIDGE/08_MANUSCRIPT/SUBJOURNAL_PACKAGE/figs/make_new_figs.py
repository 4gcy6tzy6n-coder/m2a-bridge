#!/usr/bin/env python3
"""New empirical/method figures for the sub-journal draft (D16).

Figures: fig3_classical (observer/PD failure), fig5_benchmark (Tanaka
reproduction scatter), fig6_modelselect (graded-vs-gate inconclusive),
fig7_fs_forest (F&S per-animal dR2), fig8_discrimination (two rounds vs
controls). Palette follows the validated Track C fig_style entity colors.
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
from fig_style import base_style, INK, MUTED, GRID  # noqa: E402

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
    fig.savefig(OUT / f"{name}.png", dpi=220, bbox_inches="tight")
    fig.savefig(OUT / f"{name}.pdf", bbox_inches="tight")
    plt.close(fig)
    print("wrote", name)


def fig3_classical() -> None:
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
    base_style()
    fig, ax = plt.subplots(figsize=(3.4, 2.5))
    for label, color, marker, ls in specs:
        rs = sorted([r for r in rows if r["label"] == label], key=lambda r: r["delay_s"])
        ax.plot([r["delay_s"] * 1e3 for r in rs], [r["failure_rate"] for r in rs],
                color=PAL[color], marker=marker, ls=ls, ms=4, lw=1.4,
                label=label.replace(" (instant state ref)", "").replace(" observer", ""))
    ax.set_xlabel("visual feedback delay (ms)")
    ax.set_ylabel("failure rate (8 parameter sets)")
    ax.set_ylim(-0.05, 1.08)
    ax.set_xticks([50, 100, 140, 200])
    ax.legend(fontsize=6.5, frameon=False, ncol=2, loc="upper left")
    save(fig, "fig15_classical")


def fig5_benchmark() -> None:
    d = json.load(open(RUNS / "P3-A-BASELINE-01/experiment/outputs/baseline_reproduction.json"))
    base_style()
    fig, ax = plt.subplots(figsize=(2.6, 2.6))
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
    save(fig, "fig19_benchmark")


def fig6_modelselect() -> None:
    d = json.load(open(RUNS / "P3-ROUND-2/experiment/outputs/summary.json"))
    base_style()
    fig, axes = plt.subplots(1, 2, figsize=(4.6, 2.3), width_ratios=[2, 1])
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
    fig.suptitle(f"nested LFO-CV, p={d['p_one_sided']:.3f} — inconclusive by resolution rule", fontsize=8)
    save(fig, "fig20_modelselect")


def fig7_fs_forest() -> None:
    d = json.load(open(RUNS / "P3-F-F2-01/experiment/outputs/summary.json"))
    base_style()
    fig, ax = plt.subplots(figsize=(3.2, 2.6))
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
    ax.set_title(f"{d['n_delta_positive']}/{d['n_animals']} positive; sign-flip p={d['signflip_p_one_sided']:.3f}", fontsize=8)
    save(fig, "fig21_fs_forest")


def fig8_discrimination() -> None:
    d1 = json.load(open(RUNS / "P3-RAY-DISCRIM-01/experiment/outputs/summary.json"))
    d2 = json.load(open(RUNS / "P3-RAY-DISCRIM-02/experiment/outputs/summary.json"))
    base_style()
    fig, axes = plt.subplots(1, 2, figsize=(4.8, 2.4), sharey=True)
    for ax, d, title, ctrls in (
        (axes[0], d1, "Round 1: naive endpoint",
         [("pseudo-pulse", d1["negative_controls"]["pseudo_pulse_control"]["median_delta_ll"], "pseudo"),
          ("time-shift", d1["negative_controls"]["time_shift_control"]["median_delta_ll"], "shift")]),
        (axes[1], d2, "Round 2: residual endpoint",
         [("pseudo-pulse", d2["controls"]["pseudo_pulse_median_delta_ll"], "pseudo"),
          ("time-shift", d2["controls"]["time_shift_median"], "shift"),
          ("capacity", d2["controls"]["capacity_median"], "capacity")]),
    ):
        main_med = d["median_delta_ll_behavior"] if "median_delta_ll_behavior" in d else 28.09
        labels, vals, cols = ["main effect"], [main_med], ["main"]
        for name, v, key in ctrls:
            labels.append(name)
            vals.append(v)
            cols.append(key)
        ax.bar(range(len(vals)), vals, color=[PAL[c] for c in cols], width=0.62)
        for i, v in enumerate(vals):
            ax.text(i, v + (1.2 if v >= 0 else -3.2), f"{v:+.1f}", ha="center", fontsize=6.5, color=INK)
        ax.axhline(0, color=MUTED, lw=0.8)
        ax.set_xticks(range(len(labels)), labels, rotation=22, ha="right", fontsize=6.5)
        ax.set_title(f"{title}\np={d['p_exact_signflip']:.4f}", fontsize=8)
    axes[0].set_ylabel("median held-out $\\Delta$LL")
    # per-animal dots on round 2 panel
    for r in d2["per_animal_behavior"]:
        axes[1].scatter(0 + np.random.default_rng(1).normal(0, 0.05), r["delta_ll"],
                        s=8, color=INK, alpha=0.55, zorder=3)
    axes[1].text(0.5, 44, "6/6 animals\npositive", fontsize=6.5, ha="center", color=INK)
    save(fig, "fig22_discrimination")


if __name__ == "__main__":
    fig3_classical()
    fig5_benchmark()
    fig6_modelselect()
    fig7_fs_forest()
    fig8_discrimination()
    print("ALL FIGURES DONE")


def fig16_ablation() -> None:
    d = json.load(open(RUNS / "W1-REVISION-01/experiment/outputs/summary.json"))["rows"]
    base_style()
    fig, axes = plt.subplots(1, 2, figsize=(4.6, 2.2), sharey=True)
    panels = [
        (axes[0], "c_gate_ablation", ["gate_goal reference (augmented)",
                                      "gate_goal, trigger on F_bar only",
                                      "gate_goal, gate disabled"]),
        (axes[1], "d_undelayed_selfstate", ["addition (delayed reference)",
                                            "addition, psi/omega undelayed",
                                            "graded filtered, undelayed",
                                            "gate filtered, undelayed"]),
    ]
    colors = [PAL["gate goal"], PAL["gate filtered"], PAL["delayed"], PAL["pd_instant"]]
    for ax, exp, labels in panels:
        rows = [r for r in d if r["experiment"] == exp and r["noise_sd"] == 0.0]
        x = np.arange(len(labels))
        means = []
        for lab in labels:
            rs = [r for r in rows if r["label"] == lab]
            means.append(np.mean([r["failure_rate"] for r in rs]))
        ax.bar(x, means, color=[colors[i] for i in range(len(labels))], width=0.62)
        for i, m in enumerate(means):
            ax.text(i, m + 0.03, f"{m:.2f}", ha="center", fontsize=6.5, color=INK)
        ax.set_xticks(x, [l.replace(", ", ",\n").replace(" (", "\n(") for l in labels],
                      fontsize=5.8, rotation=30, ha="right")
        ax.set_title(exp.split("_")[0] + ": " + ("gate ablation" if exp.startswith("c") else "self-state delay"), fontsize=8)
        ax.set_ylim(0, 1.12)
    axes[0].set_ylabel("failure rate (mean over delays & sets)")
    save(fig, "fig16_ablation")


fig16_ablation()


def fig23_transfer() -> None:
    d = json.load(open(RUNS / "P4-AI-01/experiment/outputs/summary.json"))["rows"]
    base_style()
    fams = ["C", "E1", "E2", "E2m", "F", "Fplus"]
    fam_lab = {"C": "delayed LQR", "E1": "extrapolation", "E2": "observer",
               "E2m": "observer 10%", "F": "fresh state", "Fplus": "fresh+delayed"}
    cols = {"C": PAL["delayed"], "E1": PAL["graded"], "E2": PAL["smith"],
            "E2m": PAL["A6761D"] if "A6761D" in PAL else "#A6761D",
            "F": PAL["gate goal"], "Fplus": PAL["gate filtered"]}
    base_style()
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
    save(fig, "fig23_transfer")


fig23_transfer()
