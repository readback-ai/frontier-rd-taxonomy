"""Draw the chain from an idea to real value, who supplies each judgment, and the loop back.

Writes results/chain.png. Needs matplotlib. The rates shown are the primary scenario's.
"""

from __future__ import annotations

from dataclasses import replace
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
from chain_model import CASES, PRIMARY, SD_RESEARCHER, Params
from matplotlib.patches import FancyArrowPatch, FancyBboxPatch

SURFACE, CARD, BAND = "#fcfcfb", "#ffffff", "#f4f3ee"
INK, SECONDARY, MUTED, EDGE = "#0b0b0b", "#52514e", "#898781", "#c3c2b7"
TRANSFER, VALIDITY = "#2a78d6", "#eb6834"  # the two links, as in the pace chart's palette
OUT = Path(__file__).parent / "results" / "chain.png"

# The chain's stages: left edge, title, what happens there. Units are hundredths of the width.
STAGE_W, STAGE_Y, STAGE_H = 17.0, 39.0, 10.0
STAGES = (
    (12.0, "Ideas", "propose candidates"),
    (32.0, "Small experiments", "the lab backs the best\nof many candidates"),
    (57.0, "Experiment at scale", "a gain on the\nlab's metric"),
    (82.0, "Real value", "research progress"),
)
# Under the chain, one column per judgment and one row per judge.
COL_W = 21.0
QUESTION_Y, QUESTION_H = 28.0, 6.6
PEOPLE_Y, AI_Y, ROW_H = 19.2, 10.4, 7.4
LABELS_X, BAND_LEFT, BAND_RIGHT = 5.5, 1.0, 90.0


def box(ax, x, y, w, h, edge=EDGE, lw=1.0, fill=CARD, z=2):
    ax.add_patch(
        FancyBboxPatch(
            (x, y),
            w,
            h,
            boxstyle="round,pad=0,rounding_size=1.2",
            fc=fill,
            ec=edge,
            lw=lw,
            zorder=z,
        )
    )


def arrow(ax, start, end, color=INK, lw=1.6):
    ax.add_patch(
        FancyArrowPatch(
            start,
            end,
            arrowstyle="-|>",
            mutation_scale=13,
            color=color,
            lw=lw,
            shrinkA=0,
            shrinkB=0,
            zorder=3,
        )  # fmt: skip
    )


def cell(ax, x, y, text, color=SECONDARY, size=8.5, weight="normal"):
    ax.text(
        x, y, text, ha="center", va="center", color=color, fontsize=size, fontweight=weight,
        linespacing=1.35, zorder=4,
    )  # fmt: skip


def main() -> None:
    p = replace(Params(), **dict(CASES)[PRIMARY])
    top = f"+{SD_RESEARCHER:.2f} SD"
    plt.rcParams.update({"font.family": "DejaVu Sans", "font.size": 10})
    fig, ax = plt.subplots(figsize=(10.0, 6.3), dpi=200)
    fig.patch.set_facecolor(SURFACE)
    ax.set_facecolor(SURFACE)
    ax.set_xlim(0, 100)
    ax.set_ylim(0, 63)
    ax.axis("off")
    fig.subplots_adjust(left=0.02, right=0.98, top=0.98, bottom=0.02)

    ax.text(1, 60.3, "From an idea to real value", color=INK, fontsize=14, fontweight="bold")
    ax.text(
        1,
        54.6,
        "Two links separate how good a candidate looks from what it is worth. People and the AI "
        "each supply ideas\nand judge the links. Rates are the primary scenario's, in SD of "
        "researcher judgment per year of progress.",
        color=SECONDARY,
        fontsize=9.2,
        linespacing=1.4,
    )

    mid = STAGE_Y + STAGE_H / 2
    edges = [x for x, *_ in STAGES]
    for x, title, what in STAGES:
        box(ax, x, STAGE_Y, STAGE_W, STAGE_H)
        cell(ax, x + STAGE_W / 2, mid + 2.6, title, color=INK, size=9.5, weight="bold")
        ax.text(
            x + STAGE_W / 2, mid - 0.2, what, ha="center", va="top", color=SECONDARY, fontsize=8.5,
            linespacing=1.3,
        )  # fmt: skip
    note = STAGE_Y + STAGE_H + 1.3
    ax.text(edges[1] + STAGE_W / 2, note, "multiplied by AI labor,\nwhich the lab chooses",
            ha="center", color=MUTED, fontsize=8.3, linespacing=1.3)  # fmt: skip
    ax.text(edges[2] + STAGE_W / 2, note, "limited by compute", ha="center", color=MUTED,
            fontsize=8.3)  # fmt: skip

    # Arrows between stages. The second and third are the two links.
    arrow(ax, (edges[0] + STAGE_W + 0.5, mid), (edges[1] - 0.5, mid))
    columns = [(edges[0] + STAGE_W / 2, STAGE_W, INK, "How good is\nthe candidate?", STAGE_Y)]
    for k, name, color, question in (
        (1, "transfer", TRANSFER, "Does the small-scale\ngain hold at scale?"),
        (2, "validity", VALIDITY, "Does the metric mean\nwhat was wanted?"),
    ):
        left, right = edges[k] + STAGE_W + 0.8, edges[k + 1] - 0.8
        arrow(ax, (left, mid), (right, mid), color=color, lw=2.4)
        cell(ax, (left + right) / 2, mid + 2.0, name, color=INK, size=9.5, weight="bold")
        columns.append(((left + right) / 2, COL_W, color, question, mid - 1.2))

    # The two judges, as bands across the columns.
    for y, name, what, fill, edge in (
        (PEOPLE_Y, "People", "judgment\nis fixed", BAND, BAND),
        (AI_Y, "AI", "judgment\nimproves", CARD, EDGE),
    ):
        box(ax, BAND_LEFT, y, BAND_RIGHT - BAND_LEFT, ROW_H, fill=fill, edge=edge, z=1)
        cell(ax, LABELS_X, y + ROW_H - 2.2, name, color=INK, size=9.5, weight="bold")
        cell(ax, LABELS_X, y + 2.4, what, color=MUTED, size=7.6)

    # A question heads each column, joined to the stage or link it is about.
    for centre, w, color, question, upto in columns:
        strong = color != INK
        box(ax, centre - w / 2, QUESTION_Y, w, QUESTION_H, edge=color, lw=1.6 if strong else 1.2)
        ax.plot([centre, centre], [QUESTION_Y + QUESTION_H, upto - 0.6], color=color, lw=1.0,
                ls=(0, (2, 2)), zorder=1)  # fmt: skip
        cell(ax, centre, QUESTION_Y + QUESTION_H / 2, question, color=INK, size=8.8)

    ideas, transfer, validity = (centre for centre, *_ in columns)
    row = PEOPLE_Y + ROW_H / 2
    cell(ax, ideas, row, f"propose their own:\nthe best is at {top}")
    cell(
        ax,
        (transfer + validity) / 2,
        row,
        "judge as many experiments as they have time for, and gains\n"
        f"up to {top} of ideas. What they judge keeps its full gain.",
    )
    row = AI_Y + ROW_H / 2
    cell(ax, ideas, row, f"replaces any worse idea:\n+{p.idea_rate:g} SD a year, no ceiling")
    cell(ax, transfer, row, f"judges the rest:\n+{p.transfer_rate:g} SD a year")
    cell(ax, validity, row, f"judges the rest:\n+{p.metric_rate:g} SD a year")

    # The loop: real progress makes better AI.
    right, low = edges[3] + STAGE_W - 4.5, 5.6
    ax.plot([right, right, LABELS_X], [STAGE_Y - 0.8, low, low], color=INK, lw=1.6, zorder=1,
            solid_joinstyle="round")  # fmt: skip
    arrow(ax, (LABELS_X, low), (LABELS_X, AI_Y - 0.6))
    ax.text(
        (LABELS_X + right) / 2,
        low - 2.7,
        "Progress makes the AI better at all three. Each idea is the better of a researcher's "
        "and the AI's.",
        ha="center",
        color=SECONDARY,
        fontsize=9,
    )

    OUT.parent.mkdir(exist_ok=True)
    fig.savefig(OUT, facecolor=SURFACE)
    print(f"wrote {OUT}")


if __name__ == "__main__":
    main()
