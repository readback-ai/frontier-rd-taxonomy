"""Draw the chain from an AI's ideas to real value, and the loop back to better AI.

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

SURFACE, CARD, INK, SECONDARY, MUTED = "#fcfcfb", "#ffffff", "#0b0b0b", "#52514e", "#898781"
EDGE = "#c3c2b7"
TRANSFER, VALIDITY = "#2a78d6", "#eb6834"  # the two links, as in the pace chart's palette
OUT = Path(__file__).parent / "results" / "chain.png"

# Stages of the chain: left edge, title, what happens there. Units are hundredths of the width.
STAGE_W, STAGE_Y, STAGE_H = 18.0, 34.0, 10.0
STAGES = (
    (2.0, "AI ideas", "propose candidates"),
    (24.0, "Small experiments", "the lab backs the best\nof many candidates"),
    (52.0, "Experiment at scale", "a gain on the\nlab's metric"),
    (80.0, "Real value", "research progress"),
)
CARD_Y, CARD_H = 19.0, 9.6  # the cards under the stages that say what each judgment decides


def box(ax, x, y, w, h, edge=EDGE, lw=1.0, fill=CARD):
    ax.add_patch(
        FancyBboxPatch(
            (x, y),
            w,
            h,
            boxstyle="round,pad=0,rounding_size=1.2",
            fc=fill,
            ec=edge,
            lw=lw,
            zorder=2,
        )
    )


def arrow(ax, start, end, color=INK, lw=1.6, style="arc3"):
    ax.add_patch(
        FancyArrowPatch(
            start,
            end,
            arrowstyle="-|>",
            mutation_scale=13,
            color=color,
            lw=lw,
            connectionstyle=style,
            shrinkA=0,
            shrinkB=0,
            zorder=3,
        )
    )


def rate(sd: float) -> str:
    return f"+{sd:g} SD a year"


def main() -> None:
    p = replace(Params(), **dict(CASES)[PRIMARY])
    plt.rcParams.update({"font.family": "DejaVu Sans", "font.size": 10})
    fig, ax = plt.subplots(figsize=(10.0, 5.6), dpi=200)
    fig.patch.set_facecolor(SURFACE)
    ax.set_facecolor(SURFACE)
    ax.set_xlim(0, 100)
    ax.set_ylim(0, 56)
    ax.axis("off")
    fig.subplots_adjust(left=0.02, right=0.98, top=0.98, bottom=0.02)

    ax.text(2, 53.5, "From an idea to real value", color=INK, fontsize=14, fontweight="bold")
    ax.text(
        2,
        49.6,
        "Two links separate how good a candidate looks from what it is worth. "
        "Rates are the primary scenario's.",
        color=SECONDARY,
        fontsize=9.5,
    )

    mid = STAGE_Y + STAGE_H / 2
    for x, title, what in STAGES:
        box(ax, x, STAGE_Y, STAGE_W, STAGE_H)
        ax.text(x + STAGE_W / 2, mid + 2.2, title, ha="center", color=INK, fontweight="bold")
        ax.text(
            x + STAGE_W / 2,
            mid - 0.4,
            what,
            ha="center",
            va="top",
            color=SECONDARY,
            fontsize=8.5,
            linespacing=1.3,
        )

    # Arrows between stages. The second and third are the two links.
    edges = [x for x, *_ in STAGES]
    arrow(ax, (edges[0] + STAGE_W + 0.8, mid), (edges[1] - 0.8, mid))
    links = (
        (1, "transfer", TRANSFER, "Does the small-scale\ngain hold at scale?", p.transfer_rate),
        (2, "validity", VALIDITY, "Does the metric mean\nwhat was wanted?", p.metric_rate),
    )
    for k, name, color, question, sd in links:
        left, right = edges[k] + STAGE_W + 0.8, edges[k + 1] - 0.8
        centre = (left + right) / 2
        arrow(ax, (left, mid), (right, mid), color=color, lw=2.4)
        ax.text(centre, mid + 1.6, name, ha="center", color=INK, fontweight="bold", fontsize=9.5)
        # A card under each link: the question it asks and how fast the AI gets better at it.
        w, h, y = 21.0, CARD_H, CARD_Y
        box(ax, centre - w / 2, y, w, h, edge=color, lw=1.6)
        ax.plot([centre, centre], [y + h, mid - 1.2], color=color, lw=1.0, ls=(0, (2, 2)), zorder=1)
        ax.text(
            centre, y + h - 1.5, question, ha="center", va="top", color=INK, fontsize=8.8,
            linespacing=1.3,
        )  # fmt: skip
        ax.text(
            centre, y + 1.5, f"AI judgment: {rate(sd)}", ha="center", color=SECONDARY, fontsize=8.5
        )

    # The same card for the AI's ideas, under the first stage.
    first = edges[0] + STAGE_W / 2
    box(ax, edges[0], CARD_Y, STAGE_W, CARD_H, edge=INK, lw=1.2)
    ax.plot([first, first], [CARD_Y + CARD_H, STAGE_Y - 0.6], color=INK, lw=1.0, ls=(0, (2, 2)),
            zorder=1)  # fmt: skip
    ax.text(
        first, CARD_Y + CARD_H - 1.5, "How good are the\ncandidates?", ha="center", va="top",
        color=INK, fontsize=8.8, linespacing=1.3,
    )  # fmt: skip
    ax.text(
        first, CARD_Y + 1.5, f"AI judgment: {rate(p.idea_rate)}", ha="center", color=SECONDARY,
        fontsize=8.5,
    )  # fmt: skip
    ax.text(
        edges[2] + STAGE_W / 2, STAGE_Y + STAGE_H + 1.4, "limited by compute", ha="center",
        color=MUTED, fontsize=8.5,
    )  # fmt: skip
    ax.text(
        edges[1] + STAGE_W / 2, STAGE_Y + STAGE_H + 1.4, "multiplied by AI labor", ha="center",
        color=MUTED, fontsize=8.5,
    )  # fmt: skip

    # Who supplies the judgment on the two links.
    y, h = 7.6, 8.6
    box(ax, 16.0, y, 68.5, h, fill="#f4f3ee", edge="#f4f3ee")
    ax.text(17.8, y + h - 2.4, "Who judges the two links", color=INK, fontweight="bold", fontsize=9)
    ax.text(
        17.8,
        y + 1.3,
        "People, for as many experiments as they have time for and for gains up to "
        f"+{SD_RESEARCHER:.2f} SD of ideas.\nThe AI judges the rest with its own transfer and "
        "metric judgment, and keeps less of the gain.",
        color=SECONDARY,
        fontsize=8.5,
        va="bottom",
        linespacing=1.4,
    )

    # The loop: real progress makes better AI.
    right, left, low = edges[3] + STAGE_W / 2, first, 4.2
    ax.plot([right, right, left], [STAGE_Y - 0.8, low, low], color=INK, lw=1.6, zorder=1,
            solid_joinstyle="round")  # fmt: skip
    arrow(ax, (left, low), (left, CARD_Y - 0.6))
    ax.text(
        (left + right) / 2, low - 2.6,
        "Progress makes better AI: its ideas, transfer and metric judgment all improve with it",
        ha="center", color=SECONDARY, fontsize=9,
    )  # fmt: skip

    OUT.parent.mkdir(exist_ok=True)
    fig.savefig(OUT, facecolor=SURFACE)
    print(f"wrote {OUT}")


if __name__ == "__main__":
    main()
