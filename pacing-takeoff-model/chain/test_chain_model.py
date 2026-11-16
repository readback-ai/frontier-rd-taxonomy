"""Checks on chain_model.py: its calibration, the AI Futures case it reduces to, and the
directions its results have to move in."""

import math
from dataclasses import replace

import numpy as np
import pytest
from chain_model import (
    CASES,
    DIFFICULTY_BOUNDS,
    DIFFICULTY_FITS,
    LABOR_REF,
    PACE_MAY,
    PACE_REF,
    POLICIES,
    T_MAY,
    T_REF,
    Params,
    Policy,
    ai_state,
    at,
    best_of,
    critical_share,
    fit_labor,
    lab_judgment,
    pace_in_november,
    pace_on,
    research,
    simulate,
    standing,
    steady_pace,
)

P = Params()
BY_CASE = {label: replace(P, **rates) for label, rates in CASES}
FAST = BY_CASE["Ideas, transfer and metrics all +3 SD a year"]
SLOW = BY_CASE["Ideas +3, transfer +1, metrics +0.5"]
SLOWEST = BY_CASE["Ideas +3, transfer and metrics +0.5"]
BY_NAME = {policy.name: policy for policy in POLICIES}
CENTRAL = BY_NAME["Comprehension audits, central"]


def months(base: dict, paced: dict, name: str = "ted_ai") -> float:
    return (paced["dates"][name] - base["dates"][name]) * 12.0


def test_defaults_reproduce_the_three_measurements():
    run = simulate(P, t_end=T_REF + 0.01)
    assert abs(pace_on(run, T_MAY) - PACE_MAY) < 0.005
    assert abs(pace_on(run, T_REF) - PACE_REF) < 0.005
    assert abs(at(run, "labor", T_REF) - 1.0 - LABOR_REF) < 0.05
    assert abs(at(run, "progress", T_REF) - P.progress_at_ref) < 0.002


def test_best_of_matches_known_values_of_the_expected_maximum():
    assert best_of(1) == 0.0
    assert abs(best_of(100) - 2.51) < 0.02
    assert abs(best_of(10_000) - 3.85) < 0.03
    assert best_of(1e6) - best_of(1e4) < best_of(1e4) - best_of(100)


def test_with_ai_links_at_peoples_level_research_is_the_ai_futures_rule():
    same = replace(
        P,
        transfer_ai_start=P.transfer_people,
        transfer_max=P.transfer_people,
        validity_ai_start=P.validity_people,
        validity_max=P.validity_people,
        value_of_selection=0.0,
    )
    base = math.exp(0.5 * same.value_per_sd**2)
    for progress in (0.5, 1.5, 2.5, 4.0):
        ai = ai_state(progress, same)
        for experiments in (1.0, 6.0, 40.0):
            lab = research(ai, same, experiments)
            expected = experiments * lab_judgment(ai["idea_sd"], same.value_per_sd) / base
            assert lab["real"] == pytest.approx(expected, rel=1e-9)
            assert lab["measured"] == pytest.approx(expected, rel=1e-9)


def test_an_experiment_left_to_todays_ai_is_worth_what_ai_futures_gives_its_judgment():
    q = replace(P, value_of_selection=0.0)
    ai = ai_state(q.progress_at_ref, q)
    lab = research(ai, q, experiments=1e9)  # so many that people judge almost none
    assert lab["covered"] < 1e-6
    assert lab["real"] / 1e9 == pytest.approx(math.exp(q.value_per_sd * q.judgment_start), rel=0.01)
    assert standing(q) > 0.0


def test_people_judge_every_experiment_on_the_base_date_and_fewer_as_experiments_multiply():
    run = simulate(SLOW, t_end=2028.0)
    assert run["covered"][0] == 1.0
    assert at(run, "covered", T_REF) < 0.9
    assert at(run, "covered", 2027.9) < at(run, "covered", T_REF)


def test_measured_progress_runs_ahead_of_real_progress_while_ai_metric_judgment_is_weak():
    run = simulate(SLOW)
    weak = run["metric_sd"] < 0.0
    assert np.all(run["measured_progress"][weak] >= run["progress"][weak] - 1e-9)
    late = np.searchsorted(run["t"], 2027.9)
    assert run["measured_progress"][late] > run["progress"][late] + 0.2


def test_slower_transfer_and_metric_judgment_bring_the_milestones_later():
    def when(transfer_rate: float, metric_rate: float) -> dict:
        return simulate(replace(P, transfer_rate=transfer_rate, metric_rate=metric_rate))["dates"]

    for name in ("researcher", "ted_ai"):
        assert when(3.0, 3.0)[name] < when(3.0, 1.0)[name] < when(3.0, 0.5)[name]
        assert when(3.0, 1.0)[name] < when(1.0, 1.0)[name] < when(0.5, 1.0)[name]
        assert when(1.0, 0.5)[name] < when(0.5, 0.5)[name]
    assert when(0.5, 0.5)["ted_ai"] - when(3.0, 3.0)["ted_ai"] > 1.5


def test_audits_delay_more_the_slower_the_ais_own_judgment():
    delay = [months(simulate(q), simulate(q, CENTRAL)) for q in (FAST, SLOW, SLOWEST)]
    assert delay[0] < 1.5
    assert delay[0] < delay[1] < delay[2]
    assert delay[2] > 9.0


def test_no_pacing_policy_brings_a_milestone_forward():
    for q in (FAST, SLOW):
        base = simulate(q)
        for policy in POLICIES[1:]:
            paced = simulate(q, policy)
            assert months(base, paced, "researcher") > -0.2
            assert months(base, paced, "ted_ai") > -0.2


def test_audits_cost_less_when_their_hours_also_count_as_judging():
    base = simulate(SLOW)
    none, half, full = (
        months(base, simulate(replace(SLOW, audit_credit=c), CENTRAL)) for c in (0.0, 0.5, 1.0)
    )
    assert full < half < none


def test_the_pace_settles_below_the_critical_share_and_runs_away_above_it():
    # Hold the AI's transfer and metric judgment still, set what it keeps of a gain, and let
    # people vouch for nothing, so the AI's own judgment is all that carries its ideas.
    def fixed(kept: float) -> Params:
        return replace(
            P,
            transfer_rate=0.0,
            metric_rate=0.0,
            transfer_ai_start=P.transfer_people * kept,
            validity_ai_start=P.validity_people,
            vouch_sd=0.0,
        )

    critical = critical_share(P)
    assert 0.5 < critical < 1.0
    assert steady_pace(critical, P) == math.inf
    for kept in (critical - 0.4, critical - 0.3):
        run = simulate(fixed(kept))
        assert run["pace"][-1] == pytest.approx(steady_pace(kept, P), rel=0.1)
    above = simulate(fixed(critical + 0.1))
    assert above["pace"][-1] > 1.4 * at(above, "pace", above["t"][-1] - 0.25)
    assert above["dates"]["ted_ai"] < simulate(fixed(critical - 0.3))["dates"]["ted_ai"] - 1.0


def test_a_tighter_compute_limit_delays_more_and_holds_back_training():
    base = simulate(SLOW)

    def limited(share: float) -> dict:
        return simulate(SLOW, Policy("limit", compute_share=share))

    third, tenth = limited(1 / 3), limited(0.1)
    assert 0.0 < months(base, third) < months(base, tenth)
    assert months(base, third) < months(base, simulate(SLOW, BY_NAME["Internal-use lag, 9 months"]))
    # Training waits for its allowance to catch up with what it has used, so for about a
    # year the third of progress that comes from more compute stops.
    waited = math.log2(3.0) / SLOW.compute_doublings
    lost = at(base, "progress", 2028.5) - at(third, "progress", 2028.5)
    assert lost > (1.0 - SLOW.software_share) * waited


def test_a_compute_limit_cuts_ai_labor_and_small_experiments_as_well_as_experiments_at_scale():
    full = ai_state(3.0, P)
    third = ai_state(3.0, P, compute=1 / 3)
    assert third["labor"] - 1.0 == pytest.approx((full["labor"] - 1.0) / 3.0)
    assert third["candidates"] < full["candidates"]
    assert third["idea_sd"] == full["idea_sd"]


def test_harder_research_delays_the_takeoff_and_raises_what_the_ai_must_keep():
    when, critical = [], []
    for difficulty, fit in DIFFICULTY_FITS.items():
        q = replace(SLOW, difficulty=difficulty, **fit)
        when.append(simulate(q)["dates"]["ted_ai"])
        critical.append(critical_share(q))
        assert abs(pace_in_november(q) - PACE_REF) < 0.005
    assert when == sorted(when)
    assert critical == sorted(critical)
    assert critical[-1] / critical[0] == pytest.approx(1.0 / 0.25)


def test_the_pace_of_2026_cannot_be_fitted_much_above_the_central_difficulty():
    central = dict(DIFFICULTY_BOUNDS)["Central"]
    easy = replace(P, volume_elasticity=0.0)
    assert pace_in_november(fit_labor(replace(easy, difficulty=central - 0.05))) >= PACE_REF
    assert pace_in_november(fit_labor(replace(easy, difficulty=central + 0.05))) < PACE_REF
