"""What the link from comprehension to human judgment changes, on one trajectory.

Runs AI Futures' Nov 10 example trajectory under the two taste models in
calibration.yml (taste -3.5 SD in Sep 2026, improving +3 or +1 SD per year of
2025 progress), with the link off and on.

Writes results/tables_link.md and results/fig7_understanding_with_no_pacing.png.
"""
from __future__ import annotations

import numpy as np

import pacing_model as pm
from aifm_adapter import DEFAULT_AIFM_PATH, ELI_AUG_2026, Q35_EXAMPLE, Aifm
from montecarlo_taste import INK, INK2, GRID, SURFACE, TASTE_AT_AC, pinned, taste_models

OUT = pm.HERE / "results"
T_END = 2040.0
SCENARIOS = ["No pacing", "Human sign-off, no comprehension standard", "Comprehension audits, light",
             "Comprehension audits, central", "Comprehension audits, strict", "Internal-use lag, 3 months"]
PATH_DATES = {"baseline": (2027.0, 2027.25, 2027.5, 2027.67), "slow": (2027.0, 2027.5, 2028.0, 2028.5, 2029.0)}


def example(cal: dict, slope: float) -> Aifm:
    params = dict(ELI_AUG_2026, **Q35_EXAMPLE)
    spec = cal["taste_models"]
    first = Aifm(dict(params, **{TASTE_AT_AC: -30.0}), DEFAULT_AIFM_PATH, cal["reference_date"], horizon=2030.0)
    m = pinned(params, first, slope, spec["level_sd"], spec["date"], DEFAULT_AIFM_PATH, cal["reference_date"])
    m.fit_supervision("anthropic", cal)
    return m


def dates(m: Aifm, policy, link) -> tuple[dict, dict]:
    m.use_calibration(m._cal, link=link)
    run = m.simulate(policy, t_end=T_END, step=0.006, stop_at="TED-AI")
    return m.summarize(run), run


def months(a: float, b: float) -> str:
    return "past 2039" if b != b else f"{(b - a) * 12:+.0f} mo"


def date(x: float) -> str:
    return "after 2039" if x != x else pm.fmt_date(x)


def at(run: dict, key: str, when: float) -> float:
    return float(np.interp(when, run["t"], run[key]))


def main() -> None:
    cal = pm.load_calibration()
    policies = {p.name: p for p in pm.standard_policies(cal)}
    out = ["# What the link from comprehension to human judgment changes", "",
           "Written by `link_effect.py`. Do not edit by hand.", "",
           "AI Futures' Nov 10 example trajectory, with AI research taste set to "
           f"{cal['taste_models']['level_sd']:+g} SD on {pm.fmt_date(cal['taste_models']['date'])}. "
           "Pacing starts Jan 1, 2027.", ""]
    paths = {}
    for model, slope in taste_models(cal).items():
        m = example(cal, slope)
        m._cal = cal
        out += [f"## Taste improves {slope:+g} SD per year of 2025 progress ({model})", "",
                f"Pace on Nov 1, 2026: {m.base_pace(cal['reference_date']):.2f}x. Automated coder: "
                f"{date(m.milestones['AC'][0])}.", "",
                "| Scenario | Link off: superhuman AI researcher | Link off: TED-AI | Link on: superhuman AI "
                "researcher | Link on: TED-AI | Link on: delay to superhuman AI researcher | Link on: delay to "
                "TED-AI |", "|---|---|---|---|---|---|---|"]
        base = {}
        for name in SCENARIOS:
            off, run_off = dates(m, policies[name], False)
            on, run = dates(m, policies[name], True)
            if name == "No pacing":
                base, paths[model] = on, (m, run, run_off)
                off_base = off
            out.append(f"| {name} | {date(off['t_sar'])} | {date(off['t_ted_ai'])} | {date(on['t_sar'])} | "
                       f"{date(on['t_ted_ai'])} | {months(base['t_sar'], on['t_sar'])} | "
                       f"{months(base['t_ted_ai'], on['t_ted_ai'])} |")
        out += ["", f"With no pacing the link moves the superhuman AI researcher by "
                f"{(base['t_sar'] - off_base['t_sar']) * 365:+.0f} days and TED-AI by "
                f"{(base['t_ted_ai'] - off_base['t_ted_ai']) * 365:+.0f} days.", "",
                "### No pacing, link on: what the lab understands", "",
                "| Date | AI research taste | Researchers with better judgment than the AI | Share of deployed "
                "value that a person understands | Researcher time spent understanding | Lab judgment against "
                "judgment with full understanding | Pace | Pace with the link off |",
                "|---|---|---|---|---|---|---|---|"]
        _, run, run_off = paths[model]
        for when in PATH_DATES[model]:
            if when > min(run["t"][-1], run_off["t"][-1]):
                continue
            cap = at(run, "progress", when)
            out.append(f"| {pm.fmt_date(when + 1e-6)} | {m.taste_sd(cap):+.1f} SD | {m.people_share(cap):.0%} | "
                       f"{at(run, 'understood_lab', when):.0%} | {at(run, 'comprehension_share', when):.0%} | "
                       f"{at(run, 'taste', when) / at(run, 'taste_people', when):.0%} | "
                       f"{at(run, 'pace', when):.1f}x | {at(run_off, 'pace', when):.1f}x |")
        out += ["", "### Depth of understanding that judgment needs", "",
                "| Hours to understand a change well enough to judge the next step, against the central audit "
                "standard | No pacing: superhuman AI researcher | No pacing: TED-AI | Central audits: delay to "
                "superhuman AI researcher | Central audits: delay to TED-AI |", "|---|---|---|---|---|"]
        for depth in (0.5, 1.0, 2.0):
            link = pm.link_from_calibration(cal, depth=depth)
            free, _ = dates(m, policies["No pacing"], link)
            audit, _ = dates(m, policies["Comprehension audits, central"], link)
            out.append(f"| {depth:g}x | {date(free['t_sar'])} | {date(free['t_ted_ai'])} | "
                       f"{months(free['t_sar'], audit['t_sar'])} | {months(free['t_ted_ai'], audit['t_ted_ai'])} |")
        out.append("")
    (OUT / "tables_link.md").write_text("\n".join(out))
    figure(cal, paths)
    print("wrote results/tables_link.md and results/fig7_understanding_with_no_pacing.png")


def figure(cal: dict, paths: dict) -> None:
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    plt.rcParams["font.family"] = "DejaVu Sans"
    colors = {"baseline": "#2a78d6", "slow": "#eb6834"}
    slopes = taste_models(cal)
    fig, ax = plt.subplots(figsize=(9.6, 4.6), facecolor=SURFACE)
    ax.set_facecolor(SURFACE)
    for side in ("top", "right", "left"):
        ax.spines[side].set_visible(False)
    ax.spines["bottom"].set_color(GRID)
    ax.tick_params(colors=INK2, labelsize=9, length=0)
    ax.grid(True, axis="y", color=GRID, linewidth=0.8)
    ax.set_axisbelow(True)
    hi = 2029.75
    for model, (m, run, _) in paths.items():
        keep = run["t"] <= hi
        ax.plot(run["t"][keep], run["understood_lab"][keep], color=colors[model], linewidth=2,
                label=f"Taste {slopes[model]:+g} SD a year")
        sd = np.array([m.taste_sd(c) for c in run["progress"]])
        for level, text in ((0.0, "AI matches the\nmedian researcher"), (3.09, "superhuman\nAI researcher")):
            if sd[-1] < level:
                continue
            when = float(np.interp(level, sd, run["t"]))
            u = float(np.interp(when, run["t"], run["understood_lab"]))
            ax.plot(when, u, "o", color=colors[model], markersize=8, markeredgecolor=SURFACE, markeredgewidth=2,
                    zorder=4)
            ax.annotate(text, (when, u), xytext=(8, 10 if level == 0.0 else 12), textcoords="offset points",
                        fontsize=8.5, color=INK2, va="bottom")
    ax.set_xlim(cal["reference_date"], hi)
    ax.set_ylim(-0.03, 1.08)
    ax.set_yticks([0.0, 0.25, 0.5, 0.75, 1.0])
    ax.set_yticklabels(["0%", "25%", "50%", "75%", "100%"])
    ticks = np.arange(2027.0, hi + 0.01, 0.5)
    ax.set_xticks(ticks)
    ax.set_xticklabels([pm.fmt_date(t + 1e-6) for t in ticks])
    ax.legend(loc="upper right", frameon=False, fontsize=9.5, labelcolor=INK)
    ax.set_title("With no pacing, a lab stops understanding what it deploys once AI judgment passes most "
                 "researchers", loc="left", fontsize=11.5, color=INK, pad=30)
    ax.text(0.0, 1.04, "Share of deployed value that a person understands, chosen by the lab. AI Futures' example "
            "trajectory, AI research taste -3.5 SD in Sep 2026.", transform=ax.transAxes, fontsize=9, color=INK2)
    fig.tight_layout()
    fig.savefig(OUT / "fig7_understanding_with_no_pacing.png", dpi=200, facecolor=SURFACE)
    plt.close(fig)


if __name__ == "__main__":
    main()
