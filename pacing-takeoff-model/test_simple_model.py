"""Checks on simple_model.py: its calibration, its closed-form results and the findings of
the full models it is meant to carry."""

import math
from dataclasses import replace

import numpy as np
from simple_model import (
    PACE_MAY,
    PACE_REF,
    POLICIES,
    T_MAY,
    T_REF,
    Params,
    calibrate,
    combine,
    critical_rate,
    pace_on,
    simulate,
    steady_pace,
)

P = Params()
ONE_FAST = replace(P, supervisable_rate=3.0, hts_fuzzy_rate=3.0)
SPLIT = replace(P, supervisable_rate=3.0, hts_fuzzy_rate=1.0)
SLOW = replace(P, supervisable_rate=3.0, hts_fuzzy_rate=0.5)
BY_NAME = {policy.name: policy for policy in POLICIES}
CENTRAL = BY_NAME["Comprehension audits, central"]


def months(base: dict, paced: dict, name: str) -> float:
    return (paced["dates"][name] - base["dates"][name]) * 12.0


def test_defaults_are_the_fit_to_the_two_measured_paces():
    fitted = calibrate(P)
    assert abs(fitted.u0 / P.u0 - 1.0) < 0.01
    assert abs(fitted.uplift_doubling / P.uplift_doubling - 1.0) < 0.01
    assert abs(fitted.progress_at_ref - P.progress_at_ref) < 0.005
    run = simulate(P, t_end=T_REF + 0.01)
    assert abs(pace_on(run, T_MAY) - PACE_MAY) < 0.01
    assert abs(pace_on(run, T_REF) - PACE_REF) < 0.01


def test_no_ai_means_the_historical_pace():
    run = simulate(replace(P, u0=0.0, judgment_start=-40.0), t_end=2030.0)
    assert np.allclose(run["pace"], 1.0, atol=1e-6)


def test_pace_settles_where_the_formula_says_below_the_critical_rate():
    for rate in (1.0, 0.5):
        slow = replace(P, supervisable_rate=rate, hts_fuzzy_rate=rate, residue=0.0)
        run = simulate(slow, t_end=2046.0)
        assert not run["ran_away"]
        assert abs(run["pace"][-1] / steady_pace(rate, P) - 1.0) < 0.03


def test_loop_runs_away_above_the_critical_rate():
    assert 2.1 < critical_rate(P) < 3.0
    assert steady_pace(3.0, P) == math.inf
    fast = simulate(ONE_FAST)
    assert fast["pace"][-1] > 5.0 * pace_on(fast, 2027.0)  # and still rising at TED-AI
    assert not simulate(replace(P, supervisable_rate=2.1, hts_fuzzy_rate=2.1), t_end=2032.0)[
        "ran_away"
    ]


def test_equal_rates_are_one_kind_of_judgment():
    for weight, substitution in ((0.5, 0.25), (0.8, 0.0), (0.65, 1.0)):
        assert (
            abs(
                combine(2.0, 2.0, replace(P, supervisable_weight=weight, substitution=substitution))
                - 2.0
            )
            < 1e-9
        )
    a = simulate(ONE_FAST)["dates"]
    b = simulate(replace(ONE_FAST, supervisable_weight=0.5, substitution=0.9))["dates"]
    assert a == b


def test_hts_fuzzy_rate_matters_more_than_supervisable_rate():
    base = simulate(SPLIT)["dates"]["ted_ai"]
    slower_supervisable = simulate(replace(SPLIT, supervisable_rate=2.1))["dates"]["ted_ai"]
    slower_hts_fuzzy = simulate(SLOW)["dates"]["ted_ai"]
    assert 0.0 <= slower_supervisable - base < 1.0
    assert slower_hts_fuzzy - base > 5.0


def test_residue_delays_more_the_slower_hts_fuzzy_judgment_improves():
    def delay(p):
        with_residue = simulate(p)["dates"]["researcher"]
        return with_residue - simulate(replace(p, residue=0.0))["dates"]["researcher"]

    assert abs(delay(ONE_FAST)) < 0.02 < delay(SPLIT) < delay(SLOW)


def test_a_lag_delays_by_about_its_length_where_judgment_is_fast():
    base = simulate(ONE_FAST)
    for name, low, high in (
        ("Internal-use lag, 3 months", 2.0, 7.0),
        ("Internal-use lag, 9 months", 5.0, 14.0),
    ):
        paced = simulate(ONE_FAST, BY_NAME[name])
        for milestone in ("researcher", "ted_ai"):
            assert low <= months(base, paced, milestone) <= high


def test_audits_delay_more_the_slower_hts_fuzzy_judgment_improves():
    fast = months(simulate(ONE_FAST), simulate(ONE_FAST, CENTRAL), "ted_ai")
    split = months(simulate(SPLIT), simulate(SPLIT, CENTRAL), "ted_ai")
    slow = months(simulate(SLOW), simulate(SLOW, CENTRAL), "ted_ai")
    assert fast < 2.0 < split < slow


def test_no_policy_brings_a_milestone_forward_and_stricter_audits_delay_more():
    for p in (ONE_FAST, SPLIT):
        base = simulate(p)
        delays = []
        for policy in POLICIES[1:]:
            paced = simulate(p, policy)
            assert months(base, paced, "researcher") > -0.1
            assert months(base, paced, "ted_ai") > -0.1
            if policy.lag == 0.0 and policy.audit_hours > 0.0:
                delays.append(months(base, paced, "ted_ai"))
        assert delays == sorted(delays)


def test_audit_delay_turns_on_how_fast_deployed_changes_grow():
    slow_growth = replace(SPLIT, change_growth=0.2)
    fast_growth = replace(SPLIT, change_growth=0.6)
    few = months(simulate(slow_growth), simulate(slow_growth, CENTRAL), "ted_ai")
    many = months(simulate(fast_growth), simulate(fast_growth, CENTRAL), "ted_ai")
    assert few < 1.0 < 6.0 < many


def test_policies_change_nothing_before_they_start():
    base = simulate(SPLIT, t_end=2027.0)
    for policy in POLICIES[1:]:
        paced = simulate(SPLIT, policy, t_end=2027.0)
        assert np.allclose(base["pace"][:-2], paced["pace"][:-2])


def test_an_audited_lab_counts_the_changes_from_the_labor_it_directs():
    """Time spent understanding is time not spent directing AI labor, so the lab deploys
    fewer changes. The share it understands is its time over the time those changes take."""
    run = simulate(SPLIT, CENTRAL)
    labor_at_ref = 1.0 + P.u0 * 2.0 ** (P.progress_at_ref / P.uplift_doubling)
    time, understood = run["time_understanding"], run["understood"]
    partial = (understood < 0.99) & (time > P.understanding_today)
    assert partial.sum() > 100
    directed = run["labor"] * (1.0 - time) / (1.0 - P.understanding_today)
    everything = P.understanding_today * (directed / labor_at_ref) ** P.change_growth
    assert np.allclose(understood[partial], (time / everything)[partial], rtol=1e-6)
