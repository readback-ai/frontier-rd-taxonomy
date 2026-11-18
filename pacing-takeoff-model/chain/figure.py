"""Draw the pace of progress in the primary scenario.

Writes results/pace.png, the pace under each pacing policy, and results/measured.png, the pace
with no pacing beside the pace the lab's own metrics show. Needs matplotlib as well as numpy.
"""

from __future__ import annotations

from dataclasses import replace
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from chain_model import (
    CASES,
    COMPUTE_LIMIT,
    CUT_THEN_HOLD,
    MONTHS,
    PACE_MAY,
    PACE_REF,
    POLICIES,
    PRIMARY,
    SPEED_LIMIT,
    T_MAY,
    T_REF,
    Params,
    fmt_date,
    simulate,
)
from matplotlib.ticker import FixedLocator, NullFormatter

SURFACE, INK, SECONDARY, MUTED = "#fcfcfb", "#0b0b0b", "#52514e", "#898781"
GRID, AXIS = "#e1e0d9", "#c3c2b7"
# Policy, legend name and line color. No pacing is the reference and takes the ink. The four
# policies take the first four slots of a palette checked for color-blind separation.
SERIES = (
    ("No pacing", "No pacing", INK),
    ("Comprehension audits", "Comprehension audits", "#2a78d6"),
    ("Internal-use lag, 9 months", "Internal-use lag, 9 months", "#eb6834"),
    ("Comprehension audits + 9-month lag", "Audits and 9-month lag", "#1baf7a"),
    (COMPUTE_LIMIT, "Compute capped at 9.6% of total", "#eda100"),
)
START, PACING, TICKS = 2026.0, 2027.0, (1.0, 1.5, 2.0, 3.0, 5.0, 10.0, 15.0)
OUT = Path(__file__).parent / "results" / "pace.png"
OUT_MEASURED = Path(__file__).parent / "results" / "measured.png"
OUT_SPEED = Path(__file__).parent / "results" / "speed.png"
MEASURED = "#2a78d6"


def frame(ax, last: float) -> None:
    """Dates along the bottom, a light grid and no box."""
    ax.set_xlim(START, last + 0.45)
    years = [year for year in range(int(START), int(last) + 2) if year <= last + 0.45]
    ax.set_xticks([float(year) for year in years])
    ax.set_xticklabels([f"{MONTHS[0]} {year}" for year in years])
    ax.grid(axis="y", which="major", color=GRID, lw=0.8)
    ax.grid(axis="y", which="minor", visible=False)
    ax.tick_params(axis="both", which="both", length=0, colors=MUTED, labelsize=9)
    for side in ("top", "right", "left"):
        ax.spines[side].set_visible(False)
    ax.spines["bottom"].set_color(AXIS)


def pace_axis(ax, top: float, bottom: float = 1.0) -> None:
    """Pace on a log scale, so that equal steps are equal multiples. `bottom` is the lowest
    pace drawn, and the axis gains a tick below 1 when a line goes under it."""
    ticks = TICKS if bottom >= 0.95 else (0.75, *TICKS)
    if top > 20.0:  # a line goes well over the usual range
        ticks = (*ticks, 30.0, 50.0)
    ax.set_yscale("log")
    ax.set_ylim(0.9 * min(1.0, bottom), 1.15 * top)
    ax.yaxis.set_major_locator(FixedLocator(ticks))
    ax.yaxis.set_minor_formatter(NullFormatter())
    ax.set_yticklabels([f"{tick:g}x" for tick in ticks])


def titles(fig, title: str, subtitle: str) -> None:
    fig.suptitle(title, x=0.065, y=0.965, ha="left", color=INK, fontsize=14, fontweight="bold")
    fig.text(
        0.065, 0.895, subtitle, ha="left", va="top", color=SECONDARY, fontsize=9.5, linespacing=1.4
    )


def fitted_points(ax, run: dict, color: str) -> None:
    """The two paces measured on METR's index, and the model's pace on metrics that is fitted
    to them. It is drawn up to the start of pacing, and the real pace runs below it."""
    early = (run["t"] >= START) & (run["t"] <= PACING)
    ax.plot(run["t"][early], run["measured_pace"][early], color=color, lw=1.4, ls=(0, (3, 2)),
            zorder=4)  # fmt: skip
    ax.plot(
        [T_MAY, T_REF], [PACE_MAY, PACE_REF], "o", ms=5, mfc=SURFACE, mec=INK, mew=1.2, zorder=5
    )
    ax.annotate("measured on\nMETR's index", (T_REF, PACE_REF), xytext=(-8, 6),
                textcoords="offset points", ha="right", color=MUTED, fontsize=8.5,
                linespacing=1.25)  # fmt: skip


def canvas(rows: int = 1, height: float = 5.6):
    plt.rcParams.update({"font.family": "DejaVu Sans", "font.size": 10})
    fig, axes = plt.subplots(rows, 1, figsize=(10.0, height), dpi=200, sharex=True)
    fig.patch.set_facecolor(SURFACE)
    for ax in [axes] if rows == 1 else axes:
        ax.set_facecolor(SURFACE)
    return fig, axes


def measured_figure(run: dict) -> None:
    """The pace with no pacing, and progress as it is and as the lab's own metrics show it.

    The lower panel is cumulative progress. The pace on the lab's metrics jumps when the lab
    changes how many agents it runs, and the running total does not."""
    fig, (above, below) = canvas(rows=2, height=7.6)
    shown = run["t"] >= START
    t, when = run["t"][shown], float(run["t"][-1])
    pace, real, metric = run["pace"][shown], run["progress"][shown], run["measured_progress"][shown]

    above.plot(t, pace, color=INK, lw=2.0, solid_capstyle="round", solid_joinstyle="round")
    above.plot([when], [pace[-1]], "o", ms=8, color=INK, mec=SURFACE, mew=2.0, zorder=4,
               clip_on=False)  # fmt: skip
    above.annotate(f"TED-AI, {fmt_date(run['dates']['ted_ai'])}", (when, pace[-1]), xytext=(-10, 0),
                   textcoords="offset points", ha="right", va="center", color=SECONDARY,
                   fontsize=9)  # fmt: skip
    fitted_points(above, run, MEASURED)
    pace_axis(above, max(TICKS[-1], float(pace.max())))
    frame(above, when)

    below.fill_between(t, real, metric, color=MEASURED, alpha=0.12, lw=0)
    for series, color, name in ((metric, MEASURED, "On the lab's metrics"), (real, INK, "Real")):
        below.plot(t, series, color=color, lw=2.0, solid_capstyle="round", solid_joinstyle="round")
        below.plot([when], [series[-1]], "o", ms=8, color=color, mec=SURFACE, mew=2.0, zorder=4,
                   clip_on=False)  # fmt: skip
        below.annotate(f"{name}\n{series[-1]:.1f} years", (when, series[-1]), xytext=(9, 0),
                       textcoords="offset points", va="center", color=SECONDARY, fontsize=9,
                       linespacing=1.3)  # fmt: skip
    below.set_ylim(0.0, 2.0 * np.ceil(float(metric.max()) / 2.0))
    below.yaxis.set_major_locator(FixedLocator(np.arange(0.0, 20.0, 2.0)))
    frame(below, when)
    below.set_xlim(START, when + 0.75)  # room for the two end labels

    for ax, head in (
        (above, "Pace: years of progress per calendar year"),
        (below, "Progress since October 2025, in years at the rate before then"),
    ):
        ax.set_title(head, loc="left", color=INK, fontsize=10, fontweight="bold", pad=8)
    fig.subplots_adjust(left=0.065, right=0.955, top=0.815, bottom=0.06, hspace=0.3)
    fig.suptitle("Real progress and progress on the lab's own metrics", x=0.065, y=0.975,
                 ha="left", color=INK, fontsize=14, fontweight="bold")  # fmt: skip
    fig.text(
        0.065, 0.925,
        "Primary scenario with no pacing: AI ideas and transfer judgment improve 3 SD a year, "
        "metric judgment 0.5 SD.\nA gain on the lab's metric is real only as far as the metric "
        "is valid.",
        ha="left", va="top", color=SECONDARY, fontsize=9.5, linespacing=1.4,
    )  # fmt: skip
    fig.savefig(OUT_MEASURED, facecolor=SURFACE)
    print(f"wrote {OUT_MEASURED}")


def speed_figure(p: Params, by_name: dict, unpaced: dict) -> None:
    """The real pace under the two speed limits, beside the pace on metrics that each holds."""
    fig, ax = canvas()
    # Policy, legend name, color, and where its end label sits clear of the lines.
    series = (
        (SPEED_LIMIT, "Speed limit: pace on metrics held to 1.7x", "#2a78d6",
         dict(xytext=(9, 2), ha="left")),
        (CUT_THEN_HOLD, "Compute cap for 6 months, then pace on metrics held", "#eda100",
         dict(xytext=(-9, 15), ha="right")),
    )  # fmt: skip
    shown = unpaced["t"] >= START
    ax.plot(unpaced["t"][shown], unpaced["pace"][shown], color=INK, lw=2.0, label="No pacing",
            solid_capstyle="round", solid_joinstyle="round", zorder=3)  # fmt: skip
    ends = [(float(unpaced["t"][-1]), float(unpaced["pace"][-1]), INK,
             fmt_date(unpaced["dates"]["ted_ai"]), dict(xytext=(8, 0), ha="left"))]  # fmt: skip
    lowest, last = 1.0, float(unpaced["t"][-1])
    for name, label, color, place in series:
        run = simulate(p, by_name[name])
        paced = run["t"] >= PACING
        shown = run["t"] >= START
        ax.plot(run["t"][shown], run["pace"][shown], color=color, lw=2.0, label=label,
                solid_capstyle="round", solid_joinstyle="round", zorder=2)  # fmt: skip
        # What the limit holds: the pace the lab's metrics show.
        ax.plot(run["t"][paced], run["measured_pace"][paced], color=color, lw=1.3,
                ls=(0, (4, 2)), zorder=1)  # fmt: skip
        lowest = min(
            lowest, float(run["pace"][shown].min()), float(run["measured_pace"][paced].min())
        )
        last = max(last, float(run["t"][-1]))
        lifted = float(run["released_pace"][-1])
        text = f"{fmt_date(run['dates']['ted_ai'])}, {lifted:,.0f}x if lifted"
        ends.append((float(run["t"][-1]), float(run["pace"][-1]), color, text, place))
    for when, pace, color, text, place in ends:
        ax.plot([when], [pace], "o", ms=8, color=color, mec=SURFACE, mew=2.0, zorder=4,
                clip_on=False)  # fmt: skip
        ax.annotate(text, (when, pace), textcoords="offset points", va="center", color=SECONDARY,
                    fontsize=9, linespacing=1.3, **place)  # fmt: skip
    fitted_points(ax, unpaced, MUTED)
    ax.axvline(PACING, color=AXIS, lw=1.0, zorder=1)
    ax.annotate("pacing starts", (PACING, 1.0), xycoords=("data", "axes fraction"),
                xytext=(5, -3), textcoords="offset points", va="top", color=MUTED,
                fontsize=9)  # fmt: skip
    pace_axis(ax, max(TICKS[-1], float(unpaced["pace"].max())), lowest)
    frame(ax, last)
    ax.set_ylabel("Pace: years of progress per calendar year", color=SECONDARY, fontsize=9)
    fig.subplots_adjust(left=0.065, right=0.955, top=0.80, bottom=0.085)
    titles(
        fig,
        "A speed limit on measured progress",
        "Primary scenario. Solid lines are the real pace. Dashed lines are the pace on the lab's "
        'metrics, which the limit holds.\nEach line ends when TED-AI arrives. "If lifted" is '
        "the pace the lab would have at once with no limit.",
    )
    ax.plot(
        [], [], color=SECONDARY, lw=1.3, ls=(0, (4, 2)), label="The same lab's pace on its metrics"
    )
    legend = ax.legend(loc="upper right", bbox_to_anchor=(1.0, 0.86), frameon=False, fontsize=9,
                       labelcolor=SECONDARY, handlelength=1.8, borderaxespad=0.6)  # fmt: skip
    for line in legend.get_lines():
        line.set_linewidth(2.0)
    fig.savefig(OUT_SPEED, facecolor=SURFACE)
    print(f"wrote {OUT_SPEED}")


def main() -> None:
    p = replace(Params(), **dict(CASES)[PRIMARY])
    by_name = {policy.name: policy for policy in POLICIES}
    fig, ax = canvas()
    ends, lowest, highest = [], 1.0, TICKS[-1]
    for name, label, color in SERIES:
        run = simulate(p, by_name[name])
        if name == "No pacing":
            unpaced = run
        shown = run["t"] >= START
        if by_name[name].lag > 0.0:
            # Under a lag the lab works with an older AI. The dotted line is the pace it would
            # have at once with its newest one: the gap is capability held back.
            paced = run["t"] >= PACING
            ax.plot(run["t"][paced], run["released_pace"][paced], color=color, lw=1.6,
                    ls=(0, (1, 1.8)), dash_capstyle="round", zorder=2)  # fmt: skip
            newest = float(run["released_pace"][-1])
            highest = max(highest, float(run["released_pace"][paced].max()))
            ax.annotate(f"{newest:.0f}x" if newest >= 10.0 else f"{newest:.1f}x",
                        (float(run["t"][-1]), newest), xytext=(6, 0), textcoords="offset points",
                        va="center", color=SECONDARY, fontsize=8.5)  # fmt: skip
        ax.plot(
            run["t"][shown],
            run["pace"][shown],
            color=color,
            lw=2.0,
            label=label,
            solid_capstyle="round",
            solid_joinstyle="round",
            zorder=3 if name == "No pacing" else 2,
        )
        ends.append((float(run["t"][-1]), float(run["pace"][-1]), color, run["dates"]["ted_ai"]))
        lowest = min(lowest, float(run["pace"][shown].min()))
        highest = max(highest, float(run["pace"][shown].max()))
    # End labels sit to the right of each end. The first sits to the left, clear of the lines
    # that end after it.
    places = {0: dict(xytext=(-8, 0), ha="right", va="center")}
    for k, (when, pace, color, ted) in enumerate(ends):
        ax.plot(
            [when], [pace], "o", ms=8, color=color, mec=SURFACE, mew=2.0, zorder=4, clip_on=False
        )
        place = places.get(k, dict(xytext=(8, 0), ha="left", va="center"))
        ax.annotate(
            fmt_date(ted),
            (when, pace),
            textcoords="offset points",
            color=SECONDARY,
            fontsize=9,
            **place,
        )
    fitted_points(ax, unpaced, MUTED)
    ax.axvline(PACING, color=AXIS, lw=1.0, zorder=1)
    ax.annotate(
        "pacing starts",
        (PACING, 1.0),
        xycoords=("data", "axes fraction"),
        xytext=(5, -3),
        textcoords="offset points",
        va="top",
        color=MUTED,
        fontsize=9,
    )
    last = max(when for when, *_ in ends)
    pace_axis(ax, highest, lowest)
    frame(ax, last)
    ax.set_ylabel("Pace: years of progress per calendar year", color=SECONDARY, fontsize=9)
    fig.subplots_adjust(left=0.065, right=0.955, top=0.80, bottom=0.085)
    titles(
        fig,
        "Pace of AI progress under four pacing policies",
        "Primary scenario: AI ideas and transfer judgment improve 3 SD a year, metric judgment "
        "0.5 SD.\nEach line ends when TED-AI arrives, at the date shown. Under a lag the lab works "
        "with a nine-month-old AI.",
    )
    ax.plot([], [], color=SECONDARY, lw=1.6, ls=(0, (1, 1.8)), dash_capstyle="round",
            label="A lagged lab's pace with its newest AI")  # fmt: skip
    legend = ax.legend(
        loc="upper left",
        bbox_to_anchor=(0.0, 0.80),
        frameon=False,
        fontsize=9,
        labelcolor=SECONDARY,
        handlelength=1.6,
        borderaxespad=0.6,
    )
    for line in legend.get_lines():
        line.set_linewidth(2.0)
    OUT.parent.mkdir(exist_ok=True)
    fig.savefig(OUT, facecolor=SURFACE)
    print(f"wrote {OUT}")
    measured_figure(unpaced)
    speed_figure(p, by_name, unpaced)


if __name__ == "__main__":
    main()
