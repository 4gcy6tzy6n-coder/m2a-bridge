#!/usr/bin/env python3
"""Redrawn manuscript figures, v2: seven big figures, each 3 columns x 2 rows.

Every big figure carries exactly six panels (a-f) on one design system.
All panels are re-plotted from the run outputs in runs/<round>/experiment/
outputs; no bitmap of an earlier figure is pasted in.

Grouping
  F1  model, efference-copy gain, adaptive control
  F2  window, V-term and threshold stress, survival
  F3  mechanism, closed-loop behaviour, gate statistics
  F4  goal feedforward and self-state necessity
  F5  delay, noise and body-parameter limits
  F6  fair comparators, ablations, command copy, AI transfer T1/T2
  F7  empirical constraints and discrimination, AI transfer T3
"""

from __future__ import annotations

import csv
import json
import sys
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import FancyArrowPatch, FancyBboxPatch

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))

import style2 as S  # noqa: E402


def leg(ax, **kw):
    return S.legend(ax, **kw)

ROOT = Path("/Users/yyl/Desktop/workshop/nature")
RUNS = ROOT / "runs"
OUT = HERE / "out"


def load(rel: str, name: str = "summary.json"):
    return json.loads((RUNS / rel / "experiment/outputs" / name).read_text())


def g(rel: str):
    return load(rel)["grid"]


GAIN = g("P1-EC-GAIN-01")
WINDOW = g("P1-EC-WINDOW-01")
VCLIP = g("P1-EC-VCLIP-01")
GATE = g("P1-EC-GATE-01")
ADAPT = g("P1-EC-ADAPTIVE-03")
COMMAND = g("P1-EC-COMMAND-01")
FFWD = g("P1-EC-FEEDFORWARD-01")
FFSTATE = g("P1-EC-FF-STATE-01")
GOALDEL = g("P1-EC-GOAL-DELAY-01")
FINE = g("P1-EC-FINEDELAY-01")
LONG = g("P1-EC-LONGDELAY-01")
NOISE = g("P1-EC-NOISE-01")
PHASE = g("P1-EC-PHASE-01")
SELFSTATE = g("P1-EC-SELFSTATE-01")
DAMP = g("P1-EC-DAMP-01")

DELAYS5 = ("0.02", "0.05", "0.1", "0.14", "0.2")
DELAYS4 = ("0.02", "0.05", "0.1", "0.2")


def fmt_ms(keys):
    return [f"{float(k) * 1000:g}" for k in keys]


def new_figure():
    fig, axes = plt.subplots(2, 3, figsize=S.FIGSIZE, constrained_layout=True)
    fig.get_layout_engine().set(w_pad=0.07, h_pad=0.10, wspace=0.07, hspace=0.10)
    return fig, axes.ravel()


# ------------------------------------------------------------------ F1
def f1(axes):
    # a: schematic of the model
    ax = axes[0]
    ax.set_axis_off()
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 6.2)
    box = dict(boxstyle="round,pad=0.32,rounding_size=0.18", lw=1.0)

    def node(x, y, w, h, text, fc, ec):
        ax.add_patch(FancyBboxPatch((x, y), w, h, facecolor=fc, edgecolor=ec,
                                    linewidth=1.0, boxstyle="round,pad=0.0,rounding_size=0.16"))
        ax.text(x + w / 2, y + h / 2, text, ha="center", va="center",
                fontsize=8.0, color=S.INK, linespacing=1.35)

    def arrow(p, q, dashed=False, color="#7A828B"):
        ax.add_patch(FancyArrowPatch(p, q, arrowstyle="-|>", mutation_scale=9,
                                     linewidth=1.0 if not dashed else 0.9,
                                     linestyle=(0, (3, 2)) if dashed else "solid",
                                     color=color, shrinkA=2, shrinkB=2))

    node(0.15, 3.05, 1.85, 1.25, "visual scene\nbar + grating", "#EEF3F9", "#9FB3C8")
    node(2.45, 3.05, 1.35, 1.25, "delay  d", "#FBEFD8", "#D9B978")
    node(4.20, 4.05, 2.30, 1.05, "bar pathway\nP, V", "#EEF3F9", "#9FB3C8")
    node(4.20, 2.25, 2.30, 1.05, "grating pathway\nk$_{opto}$", "#EEF3F9", "#9FB3C8")
    node(7.05, 3.05, 1.55, 1.25, "body\nI, $\\beta$", "#E8F3EC", "#97BFA6")
    node(8.95, 3.05, 0.95, 1.25, "heading", "#E8F3EC", "#97BFA6")

    arrow((2.00, 3.68), (2.45, 3.68))
    arrow((3.80, 3.85), (4.20, 4.45))
    arrow((3.80, 3.45), (4.20, 2.85))
    arrow((6.50, 4.45), (7.05, 3.95))
    arrow((6.50, 2.85), (7.05, 3.40))
    arrow((8.60, 3.68), (8.95, 3.68))

    node(4.20, 0.85, 4.40, 0.85, "graded EC:  filtered / unfiltered bar drive",
         "#F1EAF7", "#B9A2CF")
    ax.add_patch(FancyBboxPatch((3.55, 0.02), 5.55, 0.62, facecolor="#FBE9E6",
                                edgecolor="#D9A79C", linewidth=1.0,
                                boxstyle="round,pad=0.0,rounding_size=0.16"))
    ax.text(3.55 + 5.55 / 2, 0.33, "gating:  $k_{opto}$ = 0 while |bar drive| > threshold",
            ha="center", va="center", fontsize=7.6, color=S.INK)
    arrow((5.35, 1.70), (5.35, 2.25), dashed=True, color="#8E6FB0")
    arrow((7.10, 2.25), (7.10, 1.30), dashed=True, color="#8E6FB0")
    ax.text(0.15, 2.30, "five variants", fontsize=7.4, color=S.MUTED, va="top")
    ax.text(0.15, 2.02, "add · graded · gate", fontsize=7.4, color=S.MUTED, va="top")

    # b-d: gain x delay
    models = (("graded_sensory", "graded filtered"), ("allnone", "gate filtered"),
              ("allnone_motor", "gate unfiltered"))
    gains = ("0", "0.05", "0.25", "0.5", "0.75", "1")
    for ax, (key, label), letter in zip(axes[1:4], models, "bcd"):
        m = np.array([[GAIN[key][gg][dd] for dd in DELAYS4] for gg in gains])
        S.heat(ax, m, "delay (ms)", "" if letter != "b" else "efference-copy gain",
               fmt_ms(DELAYS4), [f"{float(x):g}" for x in gains])
        S.title(ax, letter, label)

    # e-f: adaptive
    ax = axes[4]
    modes = (("source", "squared error", "#5A6570", "o"),
             ("gradient", "signed gradient", "#0072B2", "s"),
             ("gradient_neg", "opposite sign", "#E69F00", "^"))
    x = np.arange(len(DELAYS4))
    for key, label, color, marker in modes:
        ax.plot(x, [ADAPT[key][d]["failure_rate"] for d in DELAYS4], marker=marker,
                color=color, label=label, markersize=5.2)
    ax.set_xticks(x, fmt_ms(DELAYS4))
    ax.set_xlabel("delay (ms)")
    ax.set_ylabel("failure rate")
    S.rate_axis(ax)
    leg(ax, loc="lower right", ncol=1)
    S.title(ax, "e", "adaptive failure")

    ax = axes[5]
    for key, label, color, marker in modes:
        ax.plot(x, [ADAPT[key][d]["mean_ro"] for d in DELAYS4], marker=marker,
                color=color, label=label, markersize=5.2)
    ax.set_xticks(x, fmt_ms(DELAYS4))
    ax.set_xlabel("delay (ms)")
    ax.set_ylabel("mean learned gain")
    S.style_axis(ax)
    leg(ax, loc="lower right", fontsize=6.8)
    S.title(ax, "f", "learned gain")


# ------------------------------------------------------------------ F2
def f2(axes):
    # a-b: window
    for ax, key, label, letter in ((axes[0], "allnone", "gate filtered", "a"),
                                   (axes[1], "allnone_motor", "gate unfiltered", "b")):
        x = np.arange(len(DELAYS5))
        for win, ls in (("2.5", "-"), ("6", "--"), ("10", ":")):
            ax.plot(x, [WINDOW[key][d][win]["failure_rate"] for d in DELAYS5],
                    marker="o", ls=ls, markersize=4.6,
                    color=S.COLORS["gate filtered"] if key == "allnone" else S.COLORS["gate command"],
                    label=f"{win} s window")
        ax.set_xticks(x, fmt_ms(DELAYS5))
        ax.set_xlabel("delay (ms)")
        ax.set_ylabel("failure rate")
        S.rate_axis(ax)
        leg(ax, loc="upper left")
        S.title(ax, letter, label)

    # c: V-term treatment
    ax = axes[2]
    vmodes = ("clip", "smooth", "unclipped")
    m = np.array([[VCLIP["allnone"][d][mm]["failure_rate"] for d in DELAYS4] for mm in vmodes])
    S.heat(ax, m, "delay (ms)", "V-term treatment", fmt_ms(DELAYS4),
           [{"clip": "clip", "smooth": "smooth", "unclipped": "unclipped"}[v] for v in vmodes])
    S.title(ax, "c", "V-term treatment")

    # d-e: gate threshold
    ratios = sorted(GATE["allnone"], key=float)
    for ax, mode, letter, label in ((axes[3], "clip", "d", "threshold · clip V"),
                                    (axes[4], "smooth", "e", "threshold · smooth V")):
        delays = sorted(GATE["allnone"][ratios[0]], key=float)
        m = np.array([[GATE["allnone"][r][d][mode]["failure_rate"] for d in delays] for r in ratios])
        S.heat(ax, m, "delay (ms)", "gate threshold (bar-torque units)",
               fmt_ms(delays), [f"{float(r):g}" for r in ratios])
        S.title(ax, letter, label)

    # f: survival
    ax = axes[5]
    rows = list(csv.DictReader(open(RUNS / "P1-EC-MULTISEED-01/experiment/outputs/multiseed.csv")))
    series = (("graded_sensory", "graded filtered"), ("graded_goal", "graded goal"),
              ("allnone", "gate filtered"), ("gate_command", "gate command"),
              ("gate_goal", "gate goal"))
    for model, entity in series:
        sel = [r for r in rows if r["model"] == model and float(r["delay_s"]) == 0.14]
        times = sorted(float(r["failure_time_s"]) if int(r["failure"]) else 6.0 for r in sel)
        n = len(times)
        surv = 1.0
        xs, ys = [0.0], [1.0]
        for i, t in enumerate(times):
            surv *= (n - i - 1) / (n - i) if n - i > 0 else 0.0
            xs.extend([t, t])
            ys.extend([ys[-1], surv])
        ax.plot(xs, ys, color=S.COLORS[entity], label=f"{entity} (n={n})",
                drawstyle="default", linewidth=1.6)
    ax.set_xlim(0, 6)
    ax.set_ylim(-0.03, 1.03)
    ax.set_xlabel("time (s)")
    ax.set_ylabel("failure-free fraction")
    S.style_axis(ax)
    leg(ax, loc="center right", ncol=1, fontsize=6.8)
    S.title(ax, "f", "140 ms, three seeds")


# ------------------------------------------------------------------ F3
def _schematic_panel(ax, kind: str):
    ax.set_axis_off()
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 5.6)

    def node(x, y, w, h, text, fc, ec, fs=8.0):
        ax.add_patch(FancyBboxPatch((x, y), w, h, facecolor=fc, edgecolor=ec,
                                    linewidth=1.0, boxstyle="round,pad=0.0,rounding_size=0.16"))
        ax.text(x + w / 2, y + h / 2, text, ha="center", va="center",
                fontsize=fs, color=S.INK, linespacing=1.30)

    def arrow(p, q, color="#7A828B", dashed=False):
        ax.add_patch(FancyArrowPatch(p, q, arrowstyle="-|>", mutation_scale=9,
                                     linewidth=1.0, color=color,
                                     linestyle=(0, (3, 2)) if dashed else "solid",
                                     shrinkA=2, shrinkB=2))

    node(0.10, 2.05, 1.75, 1.05, "delayed visual\nstate  (t − d)", "#FDF0E8", "#D9A17E")
    node(2.35, 2.05, 1.55, 1.05, "controller", "#E9F2FA", "#9FB3C8")
    node(4.40, 2.05, 1.55, 1.05, "bar torque\nfilter", "#F7F4EC", "#C8B98E")
    node(4.40, 0.30, 1.55, 1.05, "plant (body)", "#F7F1E6", "#C8B98E")
    arrow((1.85, 2.58), (2.35, 2.58))
    arrow((3.90, 2.58), (4.40, 2.58))
    arrow((5.18, 2.05), (5.18, 1.35))
    arrow((4.40, 0.82), (2.10, 0.82), color="#D98324", dashed=True)
    arrow((1.98, 0.85), (1.98, 2.05), color="#D98324", dashed=True)
    ax.text(0.30, 0.95, "visual feedback\nwith delay d", fontsize=7.4,
            color="#C46A1A", va="center", linespacing=1.35)

    if kind == "command":
        node(1.05, 4.20, 3.05, 1.00, "command copy\nto EC / gate", "#F7EAF4", "#C79BB8")
        arrow((2.58, 4.20), (2.58, 3.10), color="#B374A0", dashed=True)
        ax.text(4.55, 4.72, "no rescue", fontsize=8.6, color="#C0392B",
                fontweight="bold", va="center")
        ax.text(4.55, 4.20, "same as feedback", fontsize=7.4, color=S.MUTED, va="center")
    elif kind == "rescue":
        node(0.10, 3.55, 4.05, 1.10, "goal + current self-state (ψ, ω)", "#E4F2EC", "#8FBBA5")
        arrow((4.15, 4.10), (6.20, 4.10), color="#1F7A5A")
        arrow((6.20, 4.10), (6.20, 1.35), color="#1F7A5A")
        ax.text(7.10, 4.52, "rescue", fontsize=8.6, color="#1F7A5A",
                fontweight="bold", va="center")
        ax.text(7.10, 4.05, "0% failure ≤ 200 ms", fontsize=7.4, color=S.MUTED, va="center")
    else:  # delayed self-state
        node(0.10, 3.55, 4.05, 1.10, "goal + delayed self-state (t − d)", "#FCEFEA", "#D9A79C")
        arrow((4.15, 4.10), (6.20, 4.10), color="#C0603F", dashed=True)
        arrow((6.20, 4.10), (6.20, 1.35), color="#C0603F", dashed=True)
        ax.text(7.10, 4.52, "rescue lost", fontsize=8.6, color="#C0392B",
                fontweight="bold", va="center")
        ax.text(7.10, 4.05, "75–100% failure", fontsize=7.4, color=S.MUTED, va="center")


def f3(axes):
    for ax, kind, letter, label in (
        (axes[0], "command", "a", "command copy"),
        (axes[1], "rescue", "b", "fresh self-state"),
        (axes[2], "delayed", "c", "delayed self-state"),
    ):
        _schematic_panel(ax, kind)
        S.title(ax, letter, label)

    # d: heading trajectories
    ax = axes[3]
    tr = RUNS / "P1-EC-TRAJ-01/experiment/outputs"
    for fname, entity in (("addition", "addition"), ("graded_filtered", "graded filtered"),
                          ("gate_filtered", "gate filtered"), ("gate_goal", "gate goal")):
        d = np.load(tr / f"{fname}.npz")
        ax.plot(d["time"], d["heading"], color=S.COLORS[entity], label=entity, linewidth=1.3)
    dg = np.load(tr / "gate_goal.npz")
    ax.plot(dg["time"], dg["theta_bar"], color="#40474F", lw=1.0, ls=(0, (3, 2)),
            label="bar target")
    ax.set_ylim(-7.5, 7.5)
    ax.set_xlabel("time (s)")
    ax.set_ylabel("heading (rad)")
    S.style_axis(ax)
    leg(ax, loc="lower left", ncol=2, fontsize=6.4)
    S.title(ax, "d", "200 ms, 10 s window")

    # e: gate state
    ax = axes[4]
    for fname, entity in (("gate_filtered", "gate filtered"), ("gate_goal", "gate goal")):
        d = np.load(tr / f"{fname}.npz")
        duty = float(np.mean(d["gate_closed"]))
        ax.plot(d["time"], d["gate_closed"], color=S.COLORS[entity], linewidth=1.2,
                label=f"{entity} · duty {duty:.2f}")
    ax.set_ylim(-0.05, 1.18)
    ax.set_xlabel("time (s)")
    ax.set_ylabel("gate closed")
    S.style_axis(ax)
    leg(ax, loc="upper left", fontsize=7.0)
    S.title(ax, "e", "grating gate state")

    # f: gate duty vs delay
    ax = axes[5]
    x = np.arange(len(DELAYS5))
    for label, entity, marker in (("gate filtered", "gate filtered", "s"),
                                  ("gate command", "gate command", "o"),
                                  ("gate unfiltered oracle", "oracle", "^")):
        ax.plot(x, [COMMAND[label]["1"][d]["gate_duty"] for d in DELAYS5],
                marker=marker, color=S.COLORS[entity], label=label.replace(" oracle", " (oracle)"))
    ax.set_xticks(x, fmt_ms(DELAYS5))
    ax.set_xlabel("delay (ms)")
    ax.set_ylabel("gate duty cycle")
    ax.set_ylim(0, 1.0)
    S.style_axis(ax)
    leg(ax, loc="lower right", fontsize=6.8)
    S.title(ax, "f", "duty cycle vs delay")


# ------------------------------------------------------------------ F4
def f4(axes):
    x = np.arange(len(DELAYS5))
    gains = ("0.25", "0.5", "0.75", "1")
    ramp = ["#9DC3E6", "#5B93C9", "#2E6BA6", "#123E63"]

    ax = axes[0]
    ax.plot(x, [FFWD["gate filtered"]["0"][d]["failure_rate"] for d in DELAYS5],
            marker="s", color=S.COLORS["gate filtered"], label="gate filtered")
    for gain, color in zip(gains, ramp):
        ax.plot(x, [FFWD["gate goal"][gain][d]["failure_rate"] for d in DELAYS5],
                marker="o", color=color, label=f"ff = {gain}")
    ax.set_xticks(x, fmt_ms(DELAYS5))
    ax.set_xlabel("delay (ms)")
    ax.set_ylabel("failure rate")
    S.rate_axis(ax)
    leg(ax, loc="upper left", ncol=1, fontsize=7.0)
    S.title(ax, "a", "gating + goal feedforward")

    ax = axes[1]
    ax.plot(x, [FFWD["graded filtered"]["0"][d]["failure_rate"] for d in DELAYS5],
            marker="s", color=S.COLORS["graded filtered"], label="graded filtered")
    for gain, color in zip(gains, ramp):
        ax.plot(x, [FFWD["graded goal"][gain][d]["failure_rate"] for d in DELAYS5],
                marker="o", color=color, label=f"ff = {gain}")
    ax.set_xticks(x, fmt_ms(DELAYS5))
    ax.set_xlabel("delay (ms)")
    ax.set_ylabel("failure rate")
    S.rate_axis(ax)
    leg(ax, loc="center left", ncol=1, fontsize=6.8)
    S.title(ax, "b", "graded + goal feedforward")

    # c: self-state ablation
    ax = axes[2]
    base = [FFWD["gate filtered"]["0"][d]["failure_rate"] for d in ("0.1", "0.2")]
    cur = [FFSTATE["gate goal|ff=1"]["current"][d]["failure_rate"] for d in ("0.1", "0.2")]
    dele = [FFSTATE["gate goal|ff=1"]["delayed"][d]["failure_rate"] for d in ("0.1", "0.2")]
    w = 0.26
    xs = np.array([0, 1])
    ax.bar(xs - w, base, w, color=S.COLORS["gate filtered"], label="gate filtered")
    ax.bar(xs, cur, w, color="#0072B2", label="ff = 1, fresh state")
    ax.bar(xs + w, dele, w, color="#CC79A7", label="ff = 1, delayed state")
    for xi, trio in zip(xs, zip(base, cur, dele)):
        for off, v in zip((-w, 0, w), trio):
            ax.text(xi + off, v + 0.025, f"{v:.2f}", ha="center", fontsize=6.8, color=S.MUTED)
    ax.set_xticks(xs, ["100 ms", "200 ms"])
    ax.set_xlabel("visual delay")
    ax.set_ylabel("failure rate")
    ax.set_ylim(0, 1.34)
    S.style_axis(ax)
    leg(ax, loc="upper left", fontsize=6.6)
    S.title(ax, "c", "self-state ablation")

    # d: goal delay invariance
    ax = axes[3]
    gd = ("0", "0.05", "0.1", "0.2")
    gx = np.arange(len(gd))
    for vis, color, marker in (("0.1", "#0072B2", "o"), ("0.2", "#009E73", "s")):
        ax.plot(gx, [GOALDEL["gate goal|ff=1"][vis][k]["failure_rate"] for k in gd],
                marker=marker, color=color, label=f"visual {float(vis)*1000:g} ms")
    ax.plot(gx, [GOALDEL["gate filtered|ff=0"]["0.2"][k]["failure_rate"] for k in gd],
            marker="s", color=S.COLORS["gate filtered"], ls="--", label="gate filtered")
    ax.set_xticks(gx, [f"{float(k)*1000:g}" for k in gd])
    ax.set_xlabel("goal delay (ms)")
    ax.set_ylabel("failure rate")
    S.rate_axis(ax)
    leg(ax, loc="center left")
    S.title(ax, "d", "goal timing does not matter")

    # e: freshness
    ax = axes[4]
    lags = ("0", "0.01", "0.02", "0.03", "0.04", "0.05", "0.1", "0.2")
    lx = [float(v) * 1000 for v in lags]
    for key, entity, marker in (("gate goal|ff=1", "gate goal", "o"),
                                ("graded goal|ff=1", "graded goal", "D")):
        for delay, ls in (("0.1", "-"), ("0.2", (0, (4, 2)))):
            ax.plot(lx, [SELFSTATE[key][l][delay]["failure_rate"] for l in lags],
                    marker=marker, ls=ls, color=S.COLORS[entity], markersize=4.4,
                    label=f"{entity.replace(' goal', '')}, visual {float(delay)*1000:g} ms")
    ax.axhline(SELFSTATE["gate filtered"]["0.2"]["failure_rate"],
               color=S.COLORS["gate filtered"], lw=1.1, ls=":", label="gate filtered")
    ax.set_xlabel("self-state sample age (ms)")
    ax.set_ylabel("failure rate")
    S.rate_axis(ax)
    leg(ax, loc="center right", fontsize=6.6)
    S.title(ax, "e", "freshness dose–response")

    # f: damping control
    ax = axes[5]
    entries = [("gate damping 0.5e-11", "gate", 0.5), ("gate damping 1e-11", "gate", 1.0),
               ("gate damping 2e-11", "gate", 2.0), ("graded damping 1e-11", "graded", 1.0),
               ("graded damping 2e-11", "graded", 2.0)]
    for key, fam, gain in entries:
        ys = [DAMP[key][d]["failure_rate"] for d in ("0.05", "0.1", "0.2")]
        ax.plot([0.05, 0.1, 0.2], ys, marker="o" if fam == "gate" else "D",
                color="#7B5EA7" if fam == "gate" else "#009E73",
                alpha=0.45 + 0.25 * (gain / 2), markersize=4.6,
                label=f"{fam} damping {gain:g}e-11")
    ax.axhline(DAMP["gate filtered"]["0.2"]["failure_rate"],
               color=S.COLORS["gate filtered"], lw=1.1, ls=":", label="gate filtered")
    ax.set_xlabel("visual delay (s)")
    ax.set_ylabel("failure rate")
    S.rate_axis(ax)
    leg(ax, loc="lower left", fontsize=6.2)
    S.title(ax, "f", "damping without a goal")


# ------------------------------------------------------------------ F5
def f5(axes):
    # a: fine grid
    ax = axes[0]
    for key, entity in (("graded filtered|ff=0", "graded filtered"),
                        ("graded goal|ff=1", "graded goal"),
                        ("gate filtered|ff=0", "gate filtered"),
                        ("gate goal|ff=1", "gate goal")):
        delays = sorted(float(k) for k in FINE[key])
        ax.plot([d * 1000 for d in delays], [FINE[key][f"{d:g}"]["failure_rate"] for d in delays],
                marker=S.MARKERS[entity], color=S.COLORS[entity], markersize=3.4,
                label=entity)
    ax.set_xlim(0, 255)
    ax.set_xlabel("visual delay (ms)")
    ax.set_ylabel("failure rate")
    S.rate_axis(ax)
    leg(ax, loc="center right", ncol=1, fontsize=6.6)
    S.title(ax, "a", "fine grid, 6 s window")

    # b: long delays
    ax = axes[1]
    for key, entity, dashed in (("addition|ff=0", "addition", False),
                                ("graded filtered|ff=0", "graded filtered", False),
                                ("graded goal|ff=1", "graded goal", False),
                                ("gate filtered|ff=0", "gate filtered", False),
                                ("gate goal|ff=0.5", "gate goal", True),
                                ("gate goal|ff=1", "gate goal", False)):
        delays = sorted(float(k) for k in LONG[key])
        ax.plot([d * 1000 for d in delays], [LONG[key][f"{d:g}"]["failure_rate"] for d in delays],
                marker=S.MARKERS[entity], color=S.COLORS[entity], markersize=4.2,
                ls=(0, (4, 2)) if dashed else "-",
                label="gate goal ff=0.5" if dashed else entity)
    ax.set_xlim(190, 510)
    ax.set_xlabel("visual delay (ms)")
    ax.set_ylabel("failure rate")
    S.rate_axis(ax)
    leg(ax, loc="center left", fontsize=6.6)
    S.title(ax, "b", "long delays, 10 s window")

    # c-d: noise
    ticks = ("0", "1e-13", "1e-12", "1e-11")
    for ax, delay, letter in ((axes[2], "0.1", "c"), (axes[3], "0.2", "d")):
        for key, entity, dashed in (("graded filtered|ff=0", "graded filtered", False),
                                    ("graded goal|ff=1", "graded goal", False),
                                    ("gate filtered|ff=0", "gate filtered", False),
                                    ("gate goal|ff=0.5", "gate goal", True),
                                    ("gate goal|ff=1", "gate goal", False)):
            ax.plot(range(len(ticks)), [NOISE[key][n][delay]["failure_rate"] for n in ticks],
                    marker=S.MARKERS[entity], color=S.COLORS[entity], markersize=4.4,
                    ls=(0, (4, 2)) if dashed else "-",
                    label="gate goal ff=0.5" if dashed else entity)
        ax.set_xticks(range(len(ticks)), ["0", "10⁻¹³", "10⁻¹²", "10⁻¹¹"])
        ax.set_xlabel("torque noise SD (N m)")
        ax.set_ylabel("failure rate")
        S.rate_axis(ax)
        S.title(ax, letter, f"{float(delay)*1000:g} ms delay")
    axes[2].legend(loc="center right", fontsize=6.4)

    # e-f: phase diagrams
    inertia_keys = tuple(sorted(PHASE["gate filtered|ff=0"], key=float))
    drag_keys = tuple(sorted(PHASE["gate filtered|ff=0"][inertia_keys[0]], key=float))
    pd = ("0.02", "0.05", "0.1", "0.15", "0.2", "0.25", "0.3", "0.4")

    def phase_matrix(label):
        rows = []
        for inertia in inertia_keys:
            rows.append([float(np.mean([PHASE[label][inertia][dr][d]["failure_rate"]
                                        for dr in drag_keys])) for d in pd])
        return np.array(rows)

    for ax, label, letter, name in ((axes[4], "gate filtered|ff=0", "e", "gate filtered"),
                                    (axes[5], "gate goal|ff=1", "f", "gate goal, ff = 1")):
        m = phase_matrix(label)
        S.heat(ax, m, "visual delay (ms)", "inertia (×10⁻¹⁴ kg m²)",
               [f"{float(d)*1000:g}" for d in pd],
               [f"{float(k)*1e14:g}" for k in inertia_keys])
        S.title(ax, letter, name)


# ------------------------------------------------------------------ F6
def f6(axes):
    # a: fair comparators
    ax = axes[0]
    rows = [r for r in load("P2-OBSERVER-02")["rows"] if r["noise_sd"] == 0.0]
    for r in load("W1-REVISION-01")["rows"]:
        if r["experiment"] in ("a_gated_classical", "b_delay_observer") and r["noise_sd"] == 0.0:
            key = {"pd_gate (instant PD + gate)": "pd_gate",
                   "smith_dde exact": "smith_dde"}.get(r["label"])
            if key:
                rows.append({"label": key, "delay_s": r["delay_s"], "failure_rate": r["failure_rate"]})
    specs = (("delayed filtered baseline", "delayed", "o", "-"),
             ("gate filtered", "gate filtered", "s", "-"),
             ("gate goal ff=1 (instant state ref)", "gate goal", "o", "-"),
             ("instant classical PD (no gate)", "pd_instant", "D", "-"),
             ("pd_gate (instant PD + gate)", "pd_gate", "P", "-"),
             ("smith observer exact model", "smith", "^", "--"),
             ("smith_dde (delay embedded)", "smith_dde", "^", "-"))
    for label, key, marker, ls in specs:
        rs = sorted([r for r in rows if r["label"] == label], key=lambda r: r["delay_s"])
        ax.plot([r["delay_s"] * 1e3 for r in rs], [r["failure_rate"] for r in rs],
                color=S.COLORS[key], marker=marker, ls=ls, markersize=4.0, linewidth=1.4,
                label=label.replace(" (instant state ref)", "").replace(" observer", ""))
    ax.set_xticks([50, 100, 140, 200])
    ax.set_xlabel("visual feedback delay (ms)")
    ax.set_ylabel("failure rate")
    ax.set_ylim(-0.04, 1.62)
    ax.set_yticks([0, 0.25, 0.5, 0.75, 1.0])
    ax.set_yticklabels(["0", "0.25", "0.5", "0.75", "1"])
    S.style_axis(ax)
    leg(ax, loc="upper center", ncol=3, fontsize=5.9)
    S.title(ax, "a", "fair comparators")

    # b: gate ablation
    ax = axes[1]
    w1 = load("W1-REVISION-01")["rows"]
    labs = ["gate_goal reference (augmented)", "gate_goal, trigger on F_bar only",
            "gate_goal, gate disabled"]
    vals = [float(np.mean([r["failure_rate"] for r in w1
                           if r["experiment"] == "c_gate_ablation" and r["label"] == l
                           and r["noise_sd"] == 0.0])) for l in labs]
    cols = [S.COLORS["gate goal"], S.COLORS["gate filtered"], S.COLORS["delayed"]]
    ax.bar(range(3), vals, color=cols, width=0.58)
    for i, v in enumerate(vals):
        ax.text(i, v + 0.03, f"{v:.2f}", ha="center", fontsize=7.4, color=S.MUTED)
    ax.set_xticks(range(3), ["reference", "|F| trigger only", "gate disabled"])
    ax.set_ylim(0, 1.16)
    ax.set_ylabel("failure rate")
    S.style_axis(ax)
    S.title(ax, "b", "gating is conditional")

    # c: self-state lag
    ax = axes[2]
    labs = ["addition (delayed reference)", "addition, psi/omega undelayed",
            "graded filtered, undelayed", "gate filtered, undelayed"]
    vals = [float(np.mean([r["failure_rate"] for r in w1
                           if r["experiment"] == "d_undelayed_selfstate" and r["label"] == l
                           and r["noise_sd"] == 0.0])) for l in labs]
    cols = [S.COLORS["delayed"], S.COLORS["pd_instant"], S.COLORS["graded filtered"],
            S.COLORS["gate filtered"]]
    ax.bar(range(4), vals, color=cols, width=0.58)
    for i, v in enumerate(vals):
        ax.text(i, v + 0.03, f"{v:.2f}", ha="center", fontsize=7.4, color=S.MUTED)
    ax.set_xticks(range(4), ["delayed", "+fresh ψ/ω", "graded\nundelayed", "gate\nundelayed"])
    ax.set_ylim(0, 1.16)
    ax.set_ylabel("failure rate")
    S.style_axis(ax)
    S.title(ax, "c", "fresh self-state removes failure")

    # d: command copy
    ax = axes[3]
    x = np.arange(len(DELAYS5))
    for label, key, marker in (("graded filtered", "graded filtered", "s"),
                               ("graded command", "graded command", "o"),
                               ("graded unfiltered oracle", "oracle", "^")):
        ax.plot(x, [COMMAND[label]["1"][d]["failure_rate"] for d in DELAYS5],
                marker=marker, color=S.COLORS[key],
                label=label.replace("graded unfiltered oracle", "current-visual oracle"))
    ax.set_xticks(x, fmt_ms(DELAYS5))
    ax.set_xlabel("delay (ms)")
    ax.set_ylabel("failure rate")
    S.rate_axis(ax)
    leg(ax, loc="lower right", fontsize=6.8)
    S.title(ax, "d", "command copy does not rescue")

    # e-f: AI transfer T1/T2
    rows = load("P4-AI-01")["rows"]
    fams = (("C", "C · delayed LQR", "delayed", "o"),
            ("E1", "E1 · extrapolation", "graded filtered", "s"),
            ("E2", "E2 · observer", "graded command", "^"),
            ("E2m", "E2m · observer 10%", "oracle", "v"),
            ("F", "F · fresh state", "gate goal", "D"),
            ("Fplus", "F+ · fresh+delayed", "gate filtered", "P"))
    for ax, task, letter in ((axes[4], "T1", "e"), (axes[5], "T2", "f")):
        for fam, label, key, marker in fams:
            rs = sorted([r for r in rows if r["task"] == task and r["family"] == fam],
                        key=lambda r: r["delay_ms"])
            if not rs:
                continue
            ax.plot([r["delay_ms"] for r in rs], [r["failure_rate"] for r in rs],
                    color=S.COLORS[key], marker=marker, markersize=4.0,
                    linewidth=1.4, label=label)
        ax.set_xlabel("observation delay (ms)")
        ax.set_ylabel("failure rate")
        S.rate_axis(ax)
        S.title(ax, letter, f"artificial task {task}")
    axes[4].legend(loc="upper left", ncol=1, fontsize=6.2)


# ------------------------------------------------------------------ F7
def f7(axes):
    # a: T3 transfer
    ax = axes[0]
    rows = load("P4-AI-01")["rows"]
    fams = (("C", "C · delayed LQR", "delayed"), ("E1", "E1 · extrapolation", "graded filtered"),
            ("E2", "E2 · observer", "graded command"), ("E2m", "E2m · observer 10%", "oracle"),
            ("F", "F · fresh state", "gate goal"), ("Fplus", "F+ · fresh+delayed", "gate filtered"))
    for fam, label, key in fams:
        rs = sorted([r for r in rows if r["task"] == "T3" and r["family"] == fam],
                    key=lambda r: r["delay_ms"])
        ax.plot([r["delay_ms"] for r in rs], [r["failure_rate"] for r in rs],
                color=S.COLORS[key], marker="o", markersize=4.2, label=label)
    ax.set_xlabel("observation delay (ms)")
    ax.set_ylabel("failure rate")
    S.rate_axis(ax)
    leg(ax, loc="center right", fontsize=6.4)
    S.title(ax, "a", "artificial task T3")

    # b: benchmark reproduction
    ax = axes[1]
    d = load("P3-A-BASELINE-01", "baseline_reproduction.json")
    pts = []
    for br, key in (("Mi4", "Mi4"), ("T4/T5", "T4T5"), ("LPTC", "LPTC")):
        if key == "T4T5":
            for tt in ("T4", "T5"):
                e = d["T4T5"][tt]["vs_respMatPlot"]
                pts += [(br, r) for r in e["pearson_r_per_epoch"]]
        elif key == "Mi4":
            pts += [("Mi4", r) for r in d["Mi4"]["vs_respMatPlot"]["pearson_r_per_epoch"]]
        else:
            for ct in ("HS", "CH", "H2", "Hx", "FD1"):
                pts += [("LPTC", r) for r in d["LPTC"][ct]["vs_respMatPlot"]["pearson_r_per_epoch"]]
    rng = np.random.default_rng(0)
    for br in ("Mi4", "T4/T5", "LPTC"):
        rs = [r for b, r in pts if b == br]
        xx = np.full(len(rs), {"Mi4": 0, "T4/T5": 1, "LPTC": 2}[br]) + rng.normal(0, 0.055, len(rs))
        ax.scatter(xx, rs, s=16, color=S.COLORS[br], alpha=0.75,
                   edgecolor="white", linewidth=0.4, label=f"{br} (n={len(rs)})")
    ax.axhline(0.9, color=S.FAINT, lw=0.9, ls=":")
    ax.set_xticks([0, 1, 2], ["Mi4", "T4/T5", "LPTC"])
    ax.set_ylabel("per-epoch r vs source traces")
    ax.set_ylim(-0.05, 1.08)
    S.style_axis(ax)
    leg(ax, loc="center right", fontsize=6.4)
    S.title(ax, "b", "benchmark reproduction")

    # c: graded vs gated model selection
    ax = axes[2]
    d = load("P3-ROUND-2")
    deltas = [r["gated_rmse"] - r["graded_rmse"] for r in d["per_fly"]]
    ax.scatter(np.arange(len(deltas)), deltas, s=22, color=S.COLORS["gate filtered"],
               edgecolor="white", linewidth=0.5)
    ax.axhline(0, color=S.FAINT, lw=0.9)
    ax.axhline(d["delta_obs"], color=S.INK, lw=1.2, ls="--",
               label=f"median {d['delta_obs']:.3f}")
    ax.set_xlabel("held-out fly")
    ax.set_ylabel("ΔRMSE (gated − graded)")
    S.style_axis(ax)
    leg(ax, loc="lower left", fontsize=6.8)
    S.title(ax, "c", f"n = 19, p = {d['p_one_sided']:.3f}")

    # d: F&S forest
    ax = axes[3]
    d = load("P3-F-F2-01")
    vals = [r["delta_r2"] for r in d["per_animal"]]
    ys = np.arange(len(vals))[::-1]
    for y, v in zip(ys, vals):
        ax.plot([min(v, 0), max(v, 0)], [y, y], color=S.COLORS["main"], lw=1.0, alpha=0.45)
    ax.scatter(vals, ys, s=24, color=S.COLORS["main"], zorder=3,
               edgecolor="white", linewidth=0.5)
    ax.axvline(0, color=S.FAINT, lw=0.9)
    ax.axvline(d["median_delta_r2"], color=S.INK, lw=1.2, ls="--",
               label=f"median {d['median_delta_r2']:+.3f}")
    ax.fill_betweenx([-1, len(vals)], *d["bootstrap_ci95"], color=S.COLORS["graded filtered"],
                     alpha=0.18, label="bootstrap 95% CI")
    ax.set_yticks([])
    ax.set_ylim(-1, len(vals))
    ax.set_xlabel("held-out ΔR² (motor − visual history)")
    S.style_axis(ax)
    leg(ax, loc="lower right", fontsize=6.6)
    S.title(ax, "d", f"{d['n_delta_positive']}/{d['n_animals']} positive, p = {d['signflip_p_one_sided']:.3f}")

    # e-f: discrimination rounds
    d1 = load("P3-RAY-DISCRIM-01")
    d2 = load("P3-RAY-DISCRIM-02")
    for ax, dd, letter, label, ctrls in (
        (axes[4], d1, "e", "round 1 · naive endpoint",
         [("pseudo-pulse", d1["negative_controls"]["pseudo_pulse_control"]["median_delta_ll"], "pseudo"),
          ("time-shift", d1["negative_controls"]["time_shift_control"]["median_delta_ll"], "shift")]),
        (axes[5], d2, "f", "round 2 · residual endpoint",
         [("pseudo-pulse", d2["controls"]["pseudo_pulse_median_delta_ll"], "pseudo"),
          ("time-shift", d2["controls"]["time_shift_median"], "shift"),
          ("capacity", d2["controls"]["capacity_median"], "capacity")]),
    ):
        main = dd["median_delta_ll_behavior"]
        labels = ["main effect"] + [c[0] for c in ctrls]
        vals = [main] + [c[1] for c in ctrls]
        cols = [S.COLORS["main"]] + [S.COLORS[c[2]] for c in ctrls]
        ax.bar(range(len(vals)), vals, color=cols, width=0.56)
        for i, v in enumerate(vals):
            ax.text(i, v + 1.4, f"{v:+.1f}", ha="center", fontsize=7.0, color=S.MUTED)
        ax.axhline(0, color=S.FAINT, lw=0.9)
        ax.set_xticks(range(len(vals)), labels, fontsize=7.6)
        ax.set_ylabel("median held-out ΔLL")
        S.style_axis(ax)
        S.title(ax, letter, label)


FIGURES = (
    ("fig01_model_gain", f1),
    ("fig02_stress_survival", f2),
    ("fig03_mechanism_dynamics", f3),
    ("fig04_feedforward_selfstate", f4),
    ("fig05_limits_noise_body", f5),
    ("fig06_comparators_transfer", f6),
    ("fig07_empirical_constraints", f7),
)


def main() -> None:
    S.base_style()
    for stem, builder in FIGURES:
        fig, axes = new_figure()
        builder(axes)
        S.save(fig, OUT, stem)


if __name__ == "__main__":
    main()
