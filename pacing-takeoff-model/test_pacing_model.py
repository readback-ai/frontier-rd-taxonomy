"""Checks for the pacing model. Run: python -m pytest -q  (or python test_pacing_model.py)."""
import math
from pathlib import Path

import numpy as np

from dataclasses import replace

from pacing_model import (Policy, build_a, calibrate_a, deployment, first_crossing, free_deployment,
                          gate, gate_from_calibration, lab_choice, link_from_calibration, load_calibration,
                          power_mean, standard_policies, value_at)

CAL = load_calibration()


def cobb(labor):
    return np.asarray(labor, float) ** 0.5


GATE = gate_from_calibration(CAL)
LINK = link_from_calibration(CAL)
REF = 7.4          # labor uplift at which the calibrated counts hold


def test_gate_costs_little_at_the_reference_date():
    # Understanding everything deployed today takes 15% of a year. That time comes out of
    # directing AI work, so labor falls by about 15% and effort by under 10%.
    free = float(cobb(REF))
    out = gate(1.0 / REF, cobb, REF, GATE)
    assert out["kept"] > 0.95
    assert 0.90 * free < out["effort"] < free
    assert 0.10 < out["comprehension_share"] < 0.20


def test_gate_never_adds_effort_and_tightens_with_hours():
    for tau in (0.1, 0.01, 1e-3, 1e-5):
        free = float(cobb(1.0 / tau))
        last = free
        for scale in (0.5, 1.0, 2.0):
            out = gate(tau, cobb, REF, replace(GATE, hours_scale=scale))
            assert out["effort"] <= free * (1 + 1e-9)
            assert out["effort"] <= last * (1 + 1e-9)
            assert 0.0 < out["kept"] <= 1.0 and out["comprehension_share"] <= 1.0 + 1e-9
            last = out["effort"]


def test_gated_effort_still_rises_with_capability():
    # Experiments are not gated, so better AI should never lower gated effort.
    efforts = [gate(tau, cobb, REF, GATE)["effort"] for tau in (0.1, 0.01, 1e-3, 1e-4, 1e-5)]
    assert all(b >= a * (1 - 1e-6) for a, b in zip(efforts, efforts[1:]))


def test_deployed_changes_are_a_shrinking_share_of_experiments():
    shares = []
    for ratio in (1.0, 10.0, 100.0, 1000.0):
        d = free_deployment(GATE, REF * ratio, REF)
        shares.append(d["deployed"] / d["experiments"])
    assert math.isclose(shares[0], CAL["comprehension_gate"]["deployed_share_of_experiments_today"],
                        rel_tol=1e-6)
    assert all(b < a for a, b in zip(shares, shares[1:]))


def test_sign_off_costs_less_than_comprehension():
    signoff = replace(GATE, signoff_hours=CAL["comprehension_gate"]["signoff_hours_per_change"])
    for tau in (1e-3, 1e-5):
        assert gate(tau, cobb, REF, signoff)["effort"] >= gate(tau, cobb, REF, GATE)["effort"]


def test_heavier_tail_makes_the_gate_cheaper():
    light = gate(1e-5, cobb, REF, replace(GATE, tail=1.2))["effort"]
    heavy = gate(1e-5, cobb, REF, replace(GATE, tail=3.0))["effort"]
    assert light > heavy


def test_monitor_changes_grow_with_the_log_of_training_changes():
    d1 = deployment(GATE, np.array([1.0]))
    d2 = deployment(GATE, np.array([100.0]))
    training = next(t for t in GATE.types if t.name.startswith("training"))
    extra_monitor_hours = d2["monitor_hours"][0] / d1["monitor_hours"][0]
    assert math.isclose(extra_monitor_hours, 1.0 + math.log(100.0 ** training.elasticity), rel_tol=1e-6)


def test_model_a_calibration_hits_both_pace_estimates():
    m = calibrate_a(CAL)
    hist = m.simulate(t_end=m.t_ref + 0.02, supervised_from=1e9)
    assert abs(value_at(hist["t"], hist["pace"], 2026.33) - 1.2) < 2e-3
    assert abs(value_at(hist["t"], hist["pace"], m.t_ref) - 1.7) < 2e-3


def test_policies_change_nothing_before_they_start():
    m, _ = build_a(CAL, "anthropic")
    free = m.simulate(Policy(), t_end=2027.0)
    for pol in standard_policies(CAL):
        run = m.simulate(pol, t_end=2027.0)
        n = min(len(run["t"]), len(free["t"])) - 2
        assert np.allclose(run["pace"][:n], free["pace"][:n])


def test_every_mechanism_delays_sar_capability_in_model_a():
    m, _ = build_a(CAL, "anthropic")
    runs = {p.name: m.simulate(p) for p in standard_policies(CAL)}
    base = first_crossing(runs["No pacing"]["t"], runs["No pacing"]["Y"], m.Y_sar)
    for name, run in runs.items():
        when = first_crossing(run["t"], run["Y"], m.Y_sar)
        assert when >= base - 1e-6, name


def test_openai_fits_recover_the_published_trends():
    from pacing_model import openai_horizon_fit, read_data
    rows = read_data("openai_zero_intervention_success.csv")
    year = np.array([float(r["decimal_year"]) for r in rows])
    a, b, c = openai_horizon_fit(year, np.array([float(r["hours_mid"]) for r in rows]),
                                 np.array([float(r["zero_intervention_success"]) for r in rows]))
    assert 2.0 < 12.0 * c / b < 2.8                       # horizon doubling time in months
    horizon_july = 2.0 ** ((a + b * 2026.54) / c)
    assert 4.0 < horizon_july < 8.0                       # OpenAI: about half of 4-8 hour tasks
    ratio = [r for r in read_data("openai_chart_series.csv")
             if r["series"] == "agent_workdays_per_human_workday"]
    assert abs(float(ratio[-1]["value"]) - 3.1) < 0.1     # OpenAI's text: 3.1 in mid-August
    before_june = [float(r["value"]) for r in ratio if r["date"] < "2026-06-01"]
    assert max(before_june) < 1.0                         # OpenAI's text: below 1 before June
    for kind in ("openai", "openai_runtime"):
        m, _ = build_a(CAL, kind)
        assert 0.05 < m.supervision.halving < 1.0


def test_link_reproduces_measured_effort_at_the_reference_date():
    # AI judgment far below people's: the lab understands everything it deploys, which takes
    # the 15% of researcher time that measured labor uplift already includes.
    tau = (1.0 - LINK.time_today) / REF
    out = lab_choice(tau, cobb, REF, GATE, None, taste_people=1.0, taste_ai=0.17, link=LINK)
    assert out["understood"] > 0.99
    assert math.isclose(out["effort"], float(cobb(REF)), rel_tol=0.01)
    assert math.isclose(out["comprehension_share"], LINK.time_today, abs_tol=0.01)


def test_link_lab_stops_understanding_once_ai_judgment_matches_people():
    out = lab_choice(1e-3, cobb, REF, GATE, None, 2.0, 2.0, LINK)
    assert out["understood"] < 1e-6 and out["comprehension_share"] < 1e-6


def test_link_understanding_falls_as_ai_judgment_rises():
    shares = [lab_choice(1e-3, cobb, REF, GATE, None, 1.5, ai, LINK)["understood"]
              for ai in (0.2, 0.8, 1.2, 1.45, 1.5)]
    assert all(b <= a + 1e-9 for a, b in zip(shares, shares[1:]))
    assert shares[0] > 0.5 > shares[-1]


def test_link_audit_is_a_constraint_and_keeps_judgment():
    # An audited lab understands all it deploys, so it keeps people's judgment in full.
    # It can never do better than a lab free to choose what to understand.
    for tau in (0.1, 1e-2, 1e-3, 1e-5):
        for ai in (0.2, 0.9, 1.3):
            free = lab_choice(tau, cobb, REF, GATE, None, 1.4, ai, LINK)
            audit = lab_choice(tau, cobb, REF, GATE, GATE, 1.4, ai, LINK)
            assert audit["effort"] <= free["effort"] * (1 + 1e-9)
            assert math.isclose(audit["understood"], 1.0)
            assert math.isclose(audit["taste"], 1.4)


def test_link_audit_costs_nothing_while_the_lab_would_understand_everything_anyway():
    tau = (1.0 - LINK.time_today) / REF
    free = lab_choice(tau, cobb, REF, GATE, None, 1.0, 0.17, LINK)
    audit = lab_choice(tau, cobb, REF, GATE, GATE, 1.0, 0.17, LINK)
    assert audit["effort"] > 0.98 * free["effort"]


def test_link_sign_off_and_light_audits_leave_understanding_to_the_lab():
    signoff = replace(GATE, signoff_hours=CAL["comprehension_gate"]["signoff_hours_per_change"])
    light = replace(GATE, hours_scale=CAL["comprehension_gate"]["light_scale"])
    for rule, floor in ((signoff, 0.05), (light, 0.5)):
        low = lab_choice(1e-5, cobb, REF, GATE, rule, 2.0, 2.0, LINK)      # nothing to gain: no top-up
        assert math.isclose(low["understood"], floor, abs_tol=0.03)
        high = lab_choice(0.1, cobb, REF, GATE, rule, 1.0, 0.17, LINK)     # much to gain, few changes
        assert high["understood"] > 0.95


def test_link_costs_less_when_few_researchers_are_ahead_of_ai():
    everyone = lab_choice(1e-3, cobb, REF, GATE, None, 1.5, 1.2, LINK, people_share=1.0)
    few = lab_choice(1e-3, cobb, REF, GATE, None, 1.5, 1.2, LINK, people_share=0.1)
    assert few["effort"] >= everyone["effort"] and few["understood"] >= everyone["understood"]


def test_power_mean_is_pulled_toward_the_weakest_class():
    shares = [0.7, 0.3]
    assert math.isclose(float(power_mean([2.0, 2.0], shares, -0.5)), 2.0)
    assert math.isclose(float(power_mean([4.0, 1.0], shares, 0.0)), 4.0**0.7)
    means = [float(power_mean([100.0, 1.0], shares, r)) for r in (0.0, -0.5, -1.0, -3.0)]
    assert all(b < a for a, b in zip(means, means[1:]))
    # With one class free, judgment tops out at a fixed multiple of the other class.
    assert math.isclose(float(power_mean([1e30, 1.0], shares, -0.5)), 0.3 ** (1.0 / -0.5), rel_tol=1e-6)


def test_task_classes_that_move_together_change_nothing():
    one = lab_choice(1e-3, cobb, REF, GATE, None, 1.5, 1.2, LINK, people_share=0.4)
    two = lab_choice(1e-3, cobb, REF, GATE, None, [1.5, 1.5], [1.2, 1.2], LINK, people_share=0.4,
                     class_shares=[0.7, 0.3], class_r=-0.5)
    for key in ("effort", "understood", "labor", "taste"):
        assert math.isclose(one[key], two[key], rel_tol=1e-12), key


def test_lab_keeps_understanding_for_the_class_where_people_still_lead():
    # AI matches people on crisp tasks and is far behind on fuzzy ones. People's judgment
    # still pays on the fuzzy class, so the lab keeps understanding what it deploys.
    crisp_only = lab_choice(1e-3, cobb, REF, GATE, None, 2.0, 2.0, LINK)
    split = lab_choice(1e-3, cobb, REF, GATE, None, [2.0, 1.0], [2.0, 0.2], LINK,
                       class_shares=[0.7, 0.3], class_r=-0.5)
    assert crisp_only["understood"] < 1e-6
    assert split["understood"] > 0.3


def test_adapter_task_classes_reduce_to_one_taste_and_shift_effort_to_fuzzy_work():
    from aifm_adapter import DEFAULT_AIFM_PATH
    if not Path(DEFAULT_AIFM_PATH).exists():
        print("skipped: AIFM checkout not found")
        return
    from link_effect import example
    from montecarlo_taste import taste_models
    models = {m.name: m for m in taste_models(CAL)}
    single = example(CAL, models["baseline"])
    same = example(CAL, replace(models["split_1"], fuzzy=models["split_1"].crisp))
    for name in ("SAR", "TED-AI"):
        assert abs(single.levels[name] - same.levels[name]) < 1e-6, name
    split = example(CAL, models["split_1"])
    assert single.levels["SAR"] < split.levels["SAR"] < example(CAL, models["slow"]).levels["SAR"]
    early, late = split.capability_at(split.t_ref), split.levels["TED-AI"]
    share = lambda cap: split.effort_shares(split.class_tastes(cap)[1])[1]
    assert math.isclose(share(early), 1.0 - CAL["taste_split"]["crisp_share"], abs_tol=0.01)
    assert share(late) > 0.6


def test_adapter_link_matches_aifm_pace_at_the_reference_date():
    from aifm_adapter import DEFAULT_AIFM_PATH
    if not Path(DEFAULT_AIFM_PATH).exists():
        print("skipped: AIFM checkout not found")
        return
    from aifm_adapter import ELI_AUG_2026, Q35_EXAMPLE, Aifm
    m = Aifm(dict(ELI_AUG_2026, **Q35_EXAMPLE, ai_research_taste_at_coding_automation_anchor_sd=-3.0))
    assert m.taste_sd(m.capability_at(m.t_ref)) < -2.5
    m.fit_supervision("anthropic", CAL)
    m.use_calibration(CAL, link=True)
    run = m.simulate(Policy(), t_end=m.t_ref + 0.02)
    assert abs(run["pace"][0] / m.base_pace(m.t_ref) - 1.0) < 0.01
    assert run["understood"][0] > 0.99
    # Levels of milestones the AIFM run does not reach by its horizon follow from the taste schedule.
    short = Aifm(dict(ELI_AUG_2026, **Q35_EXAMPLE), horizon=2027.2)
    full = Aifm(dict(ELI_AUG_2026, **Q35_EXAMPLE))
    for name in ("SAR", "TED-AI"):
        when = float(np.interp(short.levels[name], full.base["progress"], full.base["t"]))
        assert abs(when - full.milestones[name][0]) < 0.02, name


def test_adapter_reproduces_aifm_milestones():
    from aifm_adapter import DEFAULT_AIFM_PATH
    if not Path(DEFAULT_AIFM_PATH).exists():
        print("skipped: AIFM checkout not found")
        return
    from aifm_adapter import Aifm
    m = Aifm({})
    s = m.summarize(m.simulate(supervised=False, t_end=2031.0))
    for name, (when, _) in m.milestones.items():
        got = s[f"t_{name.lower().replace('-', '_')}"]
        assert abs(got - when) < 0.02, (name, got, when)


if __name__ == "__main__":
    for name, fn in sorted(globals().items()):
        if name.startswith("test_") and callable(fn):
            fn()
            print("ok", name)
