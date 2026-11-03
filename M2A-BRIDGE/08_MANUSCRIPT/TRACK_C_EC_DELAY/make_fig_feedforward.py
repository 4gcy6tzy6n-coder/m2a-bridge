#!/usr/bin/env python3
"""Draw the goal-feedforward result and its mechanism controls."""

import json
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt

ROOT = Path("/Users/yyl/Desktop/workshop/nature")
FF = json.loads((ROOT / "runs/P1-EC-FEEDFORWARD-01/experiment/outputs/summary.json").read_text())["grid"]
STATE = json.loads((ROOT / "runs/P1-EC-FF-STATE-01/experiment/outputs/summary.json").read_text())["grid"]
GOAL_DELAY = json.loads((ROOT / "runs/P1-EC-GOAL-DELAY-01/experiment/outputs/summary.json").read_text())["grid"]
OUT = Path(__file__).resolve().parent / "fig_feedforward.png"
DELAYS = ("0.02", "0.05", "0.1", "0.14", "0.2")
X = list(range(len(DELAYS)))


def main() -> None:
    fig, axes = plt.subplots(2, 2, figsize=(9.5, 7.2), constrained_layout=True)

    # (a) gate goal across feedforward gains
    ax = axes[0, 0]
    ax.plot(X, [FF["gate filtered"]["0"][d]["failure_rate"] for d in DELAYS],
            marker="s", color="#D55E00", label="gate filtered")
    for gain, color in (("0.25", "#56B4E9"), ("0.5", "#0072B2"), ("0.75", "#009E73"), ("1", "#000000")):
        ax.plot(X, [FF["gate goal"][gain][d]["failure_rate"] for d in DELAYS],
                marker="o", color=color, label=f"gate goal ff={gain}")
    ax.set_xticks(X)
    ax.set_xticklabels(DELAYS)
    ax.set_xlabel("delay (s)")
    ax.set_ylabel("failure rate")
    ax.set_ylim(-0.05, 1.05)
    ax.set_title("a  gating with goal feedforward")
    ax.legend(frameon=False, fontsize=7, loc="upper left")

    # (b) graded goal across feedforward gains
    ax = axes[0, 1]
    ax.plot(X, [FF["graded filtered"]["0"][d]["failure_rate"] for d in DELAYS],
            marker="s", color="#E69F00", label="graded filtered")
    for gain, color in (("0.25", "#56B4E9"), ("0.5", "#0072B2"), ("0.75", "#009E73"), ("1", "#000000")):
        ax.plot(X, [FF["graded goal"][gain][d]["failure_rate"] for d in DELAYS],
                marker="o", color=color, label=f"graded goal ff={gain}")
    ax.set_xticks(X)
    ax.set_xticklabels(DELAYS)
    ax.set_xlabel("delay (s)")
    ax.set_ylabel("failure rate")
    ax.set_ylim(-0.05, 1.05)
    ax.set_title("b  graded cancellation with goal feedforward")
    ax.legend(frameon=False, fontsize=7, loc="upper left")

    # (c) self-state ablation
    ax = axes[1, 0]
    current = [
        FF["gate filtered"]["0"]["0.1"]["failure_rate"],
        FF["gate filtered"]["0"]["0.2"]["failure_rate"],
    ]
    ff_cur = [
        STATE["gate goal|ff=1"]["current"]["0.1"]["failure_rate"],
        STATE["gate goal|ff=1"]["current"]["0.2"]["failure_rate"],
    ]
    ff_del = [
        STATE["gate goal|ff=1"]["delayed"]["0.1"]["failure_rate"],
        STATE["gate goal|ff=1"]["delayed"]["0.2"]["failure_rate"],
    ]
    width = 0.25
    ax.bar([0 - width, 1 - width], current, width, color="#D55E00", label="gate filtered")
    ax.bar([0, 1], ff_cur, width, color="#0072B2", label="gate goal ff=1, current state")
    ax.bar([0 + width, 1 + width], ff_del, width, color="#CC79A7", label="gate goal ff=1, delayed state")
    ax.set_xticks([0, 1])
    ax.set_xticklabels(["100 ms", "200 ms"])
    ax.set_xlabel("visual delay")
    ax.set_ylabel("failure rate")
    ax.set_ylim(0, 1.05)
    ax.set_title("c  self-state ablation (gate goal)")
    ax.legend(frameon=False, fontsize=7)

    # (d) goal-delay invariance
    ax = axes[1, 1]
    goal_delays = ("0", "0.05", "0.1", "0.2")
    gx = list(range(len(goal_delays)))
    for visual, color, marker in (("0.1", "#0072B2", "o"), ("0.2", "#009E73", "s")):
        ax.plot(
            gx,
            [GOAL_DELAY["gate goal|ff=1"][visual][g]["failure_rate"] for g in goal_delays],
            marker=marker, color=color, label=f"gate goal ff=1, visual {float(visual)*1000:.0f} ms",
        )
    ax.plot(
        gx,
        [GOAL_DELAY["gate filtered|ff=0"]["0.2"][g]["failure_rate"] for g in goal_delays],
        marker="^", linestyle="--", color="#D55E00", label="gate filtered, visual 200 ms",
    )
    ax.set_xticks(gx)
    ax.set_xticklabels(["0", "50", "100", "200"])
    ax.set_xlabel("goal delay (ms)")
    ax.set_ylabel("failure rate")
    ax.set_ylim(-0.05, 1.05)
    ax.set_title("d  delaying the goal does not remove the benefit")
    ax.legend(frameon=False, fontsize=7, loc="upper left")

    fig.savefig(OUT, dpi=220)
    fig.savefig(OUT.with_suffix(".pdf"))
    print(OUT)


if __name__ == "__main__":
    main()
