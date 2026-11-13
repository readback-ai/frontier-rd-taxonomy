"""Figures for SIMPLE.md, drawn from simple_model.py. Needs matplotlib.

results/fig_simple_1_critical_rate.png   where the pace settles, by how fast judgment improves
results/fig_simple_2_pace_paths.png      the pace over time with no pacing, three cases
"""

from __future__ import annotations

import math
from dataclasses import replace
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from simple_model import Params, critical_rate, fmt_date, simulate, steady_pace

OUT = Path(__file__).resolve().parent / "results"
SURFACE, INK, INK2, GRID = "#fcfcfb", "#0b0b0b", "#52514e", "#e4e3df"
BLUE, ORANGE, AQUA = "#2a78d6", "#eb6834", "#1baf7a"
PACE_TICKS = (1, 2, 3, 5, 10, 20)


def frame(figsize: tuple[float, float]):
    plt.rcParams["font.family"] = "DejaVu Sans"
    fig, ax = plt.subplots(figsize=figsize, facecolor=SURFACE)
    ax.set_facecolor(SURFACE)
    for side in ("top", "right", "left"):
        ax.spines[side].set_visible(False)
    ax.spines["bottom"].set_color(GRID)
    ax.tick_params(colors=INK2, labelsize=9, length=0)
    ax.grid(True, axis="y", color=GRID, linewidth=0.8)
    ax.set_axisbelow(True)
    return fig, ax


def pace_axis(ax, top: float) -> None:
    ax.set_yscale("log")
    ax.set_ylim(0.93, top)
    ax.set_yticks(PACE_TICKS)
    ax.set_yticklabels([f"{v}x" for v in PACE_TICKS])
    ax.minorticks_off()


def titles(ax, title: str, subtitle: str) -> None:
    ax.set_title(title, loc="left", fontsize=11.5, color=INK, pad=30)
    ax.text(0.0, 1.04, subtitle, transform=ax.transAxes, fontsize=9, color=INK2)


def dot(ax, x: float, y: float, color: str) -> None:
    ax.plot(
        x, y, "o", color=color, markersize=8, markeredgecolor=SURFACE, markeredgewidth=2, zorder=4
    )


def critical_rate_figure(p: Params) -> None:
    fig, ax = frame((9.6, 4.6))
    crit = critical_rate(p)
    rates = np.linspace(0.0, crit - 0.02, 400)
    ax.plot(rates, [steady_pace(r, p) for r in rates], color=BLUE, linewidth=2)
    ax.axvspan(crit, 3.3, color=ORANGE, alpha=0.10, linewidth=0)
    ax.axvline(crit, color=GRID, linewidth=1)
    ax.text(
        crit + 0.05,
        11.0,
        f"Above {crit:.1f} SD a year\nthe loop runs away",
        fontsize=9.5,
        color=INK,
        va="center",
    )
    marks = (
        (0.5, "Fuzzy tasks, +0.5 SD", (-8, 8)),
        (1.0, "Fuzzy tasks, +1 SD", (-8, 8)),
        (2.1, "AI Futures' filtered\nmedian, +2.1 SD", (-10, 6)),
    )
    for rate, text, offset in marks:
        pace = steady_pace(rate, p)
        dot(ax, rate, pace, BLUE)
        ax.annotate(
            f"{text}: {pace:.1f}x",
            (rate, pace),
            xytext=offset,
            textcoords="offset points",
            fontsize=8.5,
            color=INK2,
            ha="right" if offset[0] < 0 else "left",
            va="bottom" if offset[1] > 0 else "top",
        )
    ax.plot(3.0, 24.0, "^", color=ORANGE, markersize=9, markeredgecolor=SURFACE, markeredgewidth=2)
    ax.text(
        3.0, 19.5, "AI Futures' base\ncase, +3 SD", fontsize=8.5, color=INK2, ha="center", va="top"
    )
    pace_axis(ax, 30.0)
    ax.set_xlim(0.0, 3.3)
    ax.set_xticks(np.arange(0.0, 3.01, 0.5))
    ax.set_xlabel(
        "Research judgment the AI gains per year of progress, in SD of human researchers",
        fontsize=9,
        color=INK2,
        labelpad=8,
    )
    titles(
        ax,
        "Below a critical rate of judgment improvement the pace settles; above it the loop "
        "runs away",
        "Pace of AI progress once AI labor is at its ceiling, as a multiple of the rate before "
        "October 2025. Closed form.",
    )
    fig.tight_layout()
    fig.savefig(OUT / "fig_simple_1_critical_rate.png", dpi=200, facecolor=SURFACE)
    plt.close(fig)


def pace_paths_figure(p: Params) -> None:
    fig, ax = frame((9.6, 4.8))
    hi, top = 2034.0, 30.0
    below, above = dict(xytext=(8, -4), va="top"), dict(xytext=(0, 9), va="bottom", ha="center")
    cases = (
        ("One judgment, +3 SD a year", dict(crisp_rate=3.0, fuzzy_rate=3.0), BLUE, below),
        ("Crisp +3, fuzzy +1 SD a year", dict(crisp_rate=3.0, fuzzy_rate=1.0), ORANGE, above),
        ("Crisp +3, fuzzy +0.5 SD a year", dict(crisp_rate=3.0, fuzzy_rate=0.5), AQUA, above),
    )
    for label, rates, color, place in cases:
        q = replace(p, **rates)
        run = simulate(q)
        keep = (run["t"] >= 2026.0) & (run["t"] <= hi) & (run["pace"] <= top)
        ax.plot(run["t"][keep], run["pace"][keep], color=color, linewidth=2, label=label)
        for name, text in (("researcher", "researcher-level AI"), ("ted_ai", "TED-AI")):
            when = run["dates"][name]
            pace = float(np.interp(when, run["t"], run["pace"])) if when == when else math.nan
            if not (when <= hi and pace <= top):
                continue
            dot(ax, when, pace, color)
            ax.annotate(
                f"{text}\n{fmt_date(when)}",
                (when, pace),
                textcoords="offset points",
                fontsize=8.5,
                color=INK2,
                **place,
            )
    pace_axis(ax, top)
    ax.set_xlim(2026.0, hi)
    ax.set_xticks(np.arange(2026.0, hi + 0.01, 1.0))
    ax.set_xticklabels([f"{int(y)}" for y in np.arange(2026.0, hi + 0.01, 1.0)])
    ax.legend(loc="upper right", frameon=False, fontsize=9.5, labelcolor=INK)
    titles(
        ax,
        "The rate on fuzzy tasks decides whether the pace explodes or settles",
        "Pace of AI progress with no pacing, as a multiple of the rate before October 2025. "
        "Each line ends at TED-AI or at 2034.",
    )
    fig.tight_layout()
    fig.savefig(OUT / "fig_simple_2_pace_paths.png", dpi=200, facecolor=SURFACE)
    plt.close(fig)


if __name__ == "__main__":
    params = Params()
    critical_rate_figure(params)
    pace_paths_figure(params)
    print("wrote results/fig_simple_1_critical_rate.png and results/fig_simple_2_pace_paths.png")
