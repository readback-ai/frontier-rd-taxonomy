"""Model B: the AI Futures Model (AIFM) with pacing mechanisms added.

This module does not reimplement AIFM. It imports the AI Futures Project's
public code (github.com/AI-Futures-Project/aifm-public, MIT license, commit
1c40ecd of 2026-09-09), lets that code calibrate itself and produce its own
trajectory, then integrates forward again from the reference date using the
same component functions with three additions:

  1. a supervision floor on human time per unit of coding work,
  2. the gate on production-bound work from pacing_model.gate,
  3. the internal-use lag and R&D compute policies,
  4. optionally, the link from comprehension to human research judgment
     (pacing_model.lab_choice): people's judgment counts only on the
     deployed changes they understand.

With no additions the re-integration reproduces AIFM's own milestone dates,
which test_pacing_model.py checks.
"""

from __future__ import annotations

import logging
import math
import os
import sys
from dataclasses import replace
from pathlib import Path

import numpy as np
from pacing_model import (
    Link,
    Policy,
    Supervision,
    first_crossing,
    fit_supervision,
    free_deployment,
    gate,
    gate_from_calibration,
    lab_choice,
    link_from_calibration,
    power_mean,
    value_at,
)
from scipy.optimize import brentq

# Where the AI Futures Project's public code is checked out. Set AIFM_PATH, or pass a path
# to the scripts that take --aifm-path.
DEFAULT_AIFM_PATH = Path(os.environ.get("AIFM_PATH", "~/aifm-public")).expanduser()

# The public code (2026-09-09) ships August 2026 parameter presets. AI Futures'
# 2026-11-10 update reports that those presets gave under 4% to the pace METR
# then estimated, and publishes an example trajectory for its first hypothesis
# ("more uplift from near-AC coding skills"): Eli Lifland's August preset with
# the five changes in Q35_EXAMPLE. That example is Model B's base case.
# Source for the preset: constants/parameters.ts, 'eli-08-16-26'.
ELI_AUG_2026 = dict(
    taste_schedule_type="SDs per progress-year",
    present_doubling_time=0.37488146126475763,
    ac_time_horizon_minutes=7.176091259055681,
    doubling_difficulty_growth_factor=0.92,
    rho_coding_labor=-2.0,
    rho_experiment_capacity=-0.155,
    alpha_experiment_capacity=0.809,
    direct_input_exp_cap_ces_params=False,
    r_software=2.4,
    software_progress_rate_at_reference_year=1.0,
    coding_labor_normalization=1.0,
    experiment_compute_exponent=0.655,
    parallel_penalty=0.5,
    automation_fraction_at_coding_automation_anchor=1.0,
    automation_interp_type="logistic",
    automation_logistic_asymptote=1.1,
    ai_research_taste_at_coding_automation_anchor_sd=0.5,
    ai_research_taste_slope=2.1,
    present_day=2026.578082,
    present_horizon=186.0,
    horizon_extrapolation_type="decaying doubling time",
    ac_anchor_mode="uplift-solved",
    horizon_reference_date=2026.269178,
    revenue_reference_date=2026.374429,
    eci_reference_date=2026.524658,
    present_revenue=4.7e10,
    present_revenue_growth_rate=5.0,
    revenue_required_for_ac=7e12,
    serial_uplift_at_reference_date=1.7,
    excess_uplift_doubling_time=6.500769185258003,
    uplift_reference_date=2026.578082,
    eci_at_present_day=162.0,
    eci_growth_rate=15.0,
    eci_required_for_ac=250.0,
    inf_labor_asymptote=15.142135623730951,
    inf_compute_asymptote=1001.0,
    labor_anchor_exp_cap=1.6,
    inv_compute_anchor_exp_cap=2.794435844492636,
    gap_years=0.7,
    coding_automation_efficiency_slope=3.0,
    max_serial_coding_labor_multiplier=1e8,
    median_to_top_taste_multiplier=3.698147512646408,
    top_percentile=0.999,
    taste_limit=8.0,
    taste_limit_smoothing=0.5,
    strat_ai_m2b=2.0,
    ted_ai_m2b=1.4966629547095764,
    optimal_ces_eta_init=0.05,
)
Q35_EXAMPLE = dict(
    serial_uplift_at_reference_date=7.052322627593112,  # Aug 2026 coding uplift
    excess_uplift_doubling_time=3.0130366136756046,  # months
    rho_coding_labor=-0.5,  # coding labor substitutability, -2 -> -0.5
    inf_labor_asymptote=60.0,  # infinite coding labor asymptote, 15 -> 60
    inv_compute_anchor_exp_cap=1.5,  # slowdown from 10x less experiment compute, 2.8 -> 1.5
)
# Earlier base for this briefing: the repository defaults (Daniel Kokotajlo's
# August medians) with the same hypothesis and a tuned uplift doubling time.
METR_CONDITIONED = {k: v for k, v in Q35_EXAMPLE.items() if k != "excess_uplift_doubling_time"}


def published_example(aifm_path: Path | str | None = None, t_ref: float = 2026.83) -> Aifm:
    """AI Futures' 2026-11-10 example trajectory, run on the public code."""
    return Aifm(dict(ELI_AUG_2026, **Q35_EXAMPLE), aifm_path or DEFAULT_AIFM_PATH, t_ref)


class Aifm:
    def __init__(
        self,
        overrides: dict | None = None,
        aifm_path: Path | str = DEFAULT_AIFM_PATH,
        t_ref: float = 2026.83,
        horizon: float = 2040.0,
    ):
        aifm_path = Path(aifm_path)
        if str(aifm_path) not in sys.path:
            sys.path.insert(0, str(aifm_path))
        logging.disable(logging.WARNING)  # AIFM logs every calibration step
        import progress_model.integration as integ
        from progress_model import Parameters, ProgressModel, load_time_series_data
        from progress_model import config as cfg
        from progress_model import progress_rate as pr
        from progress_model.ces_functions import compute_coding_labor_deprecated

        self.cfg, self.pr, self._human_labor = cfg, pr, compute_coding_labor_deprecated
        self.data = load_time_series_data(str(aifm_path / "inputs" / "input_data.csv"))
        self.params = Parameters(**(overrides or {}))
        self.t_ref = t_ref

        # Record the initial research stock that AIFM passes to its own ODE.
        seen = {}
        original = integ.progress_rate_at_time

        def recorder(t, state, data, params, RS_0=None, **kw):
            if RS_0 is not None and not getattr(params, "human_only", False):
                seen["RS_0"] = RS_0
            return original(t, state, data, params, RS_0=RS_0, **kw)

        integ.progress_rate_at_time = recorder
        try:
            model = ProgressModel(self.params, self.data)
            model.compute_progress_trajectory([2019.0, horizon])
        finally:
            integ.progress_rate_at_time = original
        self.RS_0 = seen["RS_0"]
        r = model.results
        self.base = {
            "t": np.asarray(r["times"], float),
            "progress": np.asarray(r["progress"], float),
            "RS": np.asarray(r["research_stock"], float),
            "rate": np.asarray(r["progress_rates"], float),
            "coding_mult": np.asarray(r["serial_coding_labor_multipliers"], float),
        }
        b = self.base
        self.rate0 = float(b["rate"][(b["t"] >= 2024.0) & (b["t"] <= 2025.5)].mean())
        # milestones: name -> (date in AIFM's own run, progress level), for those AIFM reaches
        # before `horizon`. levels: name -> progress level, for every milestone, reached or not.
        # AIFM defines the automated coder as a progress level and SAR, TED-AI and ASI as levels
        # of AI research taste, so each progress level follows from the parameters. Reading the
        # level off AIFM's trajectory at the reported date is unreliable when progress is
        # explosive: the trajectory can climb tens of orders of magnitude between two grid points.
        self.milestones, self.levels, self.targets = {}, {}, {}
        self.classes, self.class_r = None, 0.0  # research task classes, set by set_taste_classes
        p = self.params
        for key, name in (
            ("AC", "AC"),
            ("SAR-level-experiment-selection-skill", "SAR"),
            ("TED-AI", "TED-AI"),
            ("ASI", "ASI"),
        ):
            record = r["milestones"].get(key, {})
            when = record.get("time")
            level = None
            if record.get("metric") == "ai_research_taste_sd":
                self.targets[name] = (float(record["target"]), bool(record.get("requires_ac")))
            if record.get("metric") == "ai_research_taste_sd" and p.ai_research_taste_slope > 0:
                level = (
                    p.progress_at_aa
                    + (record["target"] - p.ai_research_taste_at_coding_automation_anchor_sd)
                    / p.ai_research_taste_slope
                )
                if record.get("requires_ac"):
                    level = max(level, p.progress_at_aa)
            elif record.get("metric") == "progress":
                level = record["target"]
            elif when is not None:
                level = np.interp(when, b["t"], b["progress"])
            if level is not None:
                self.levels[name] = float(level)
                if when is not None:
                    self.milestones[name] = (float(when), float(level))
        self.supervision = Supervision("none")
        self.labor_ref = float(np.interp(t_ref, b["t"], b["coding_mult"]))
        self.changes = None  # deployed-change counts, set by use_calibration
        self.link = None  # the comprehension-to-judgment link, set by use_calibration
        self.residue = 0.0  # share of work that needs a person today, set by use_calibration

    def use_calibration(
        self, cal: dict, link: bool | Link = False, residue: bool | float = False
    ) -> None:
        self.changes = gate_from_calibration(cal)
        self.residue = (
            float(cal["real_research"]["residue_today"]) if residue is True else float(residue)
        )
        self.link = link_from_calibration(cal) if link is True else (link or None)
        if self.link is not None:
            # Today only researchers whose judgment beats the AI's need to keep up.
            today = self.link.time_today * self.people_share(self.capability_at(self.t_ref))
            self.link = replace(self.link, time_today=today)

    # ---- research task classes --------------------------------------------
    def set_taste_classes(self, classes: list[dict], substitution: float) -> None:
        """Split research into classes of task whose AI judgment improves at different rates.

        classes: one dict per class with `share` (share of research effort on the class when
        judgment is equal across classes), `slope` (SD of AI judgment per unit of progress),
        `level` (SD at progress `at`). substitution: elasticity of substitution between the
        classes. Below 1 they are complements and the slowest class comes to dominate effort.

        The lab's judgment is the power mean of the classes' judgment (pacing_model.power_mean).
        A milestone AIFM defines as a level of AI research taste is reached when the judgment
        of an AI-only lab, the power mean of AI judgment across classes, reaches that level.
        """
        self.classes, self.class_r = [dict(c) for c in classes], substitution - 1.0
        td = self.params.taste_distribution
        shares = [c["share"] for c in self.classes]

        def own(c, sd):
            """Progress at which class `c` alone reaches `sd`."""
            return c["at"] + (sd - c["level"]) / c["slope"]

        def ai_only(cap):
            return float(power_mean(self.class_tastes(cap)[0], shares, self.class_r))

        for name, (target, needs_ac) in self.targets.items():
            want = float(td.get_taste_at_sd(target))
            # The lab reaches the target no sooner than its fastest class and no later than
            # its slowest, so the level lies between the two classes' own levels.
            lo, hi = (f(own(c, target) for c in self.classes) for f in (min, max))
            if hi - lo < 1e-9 or ai_only(hi) <= want:
                level = hi
            elif ai_only(lo) >= want:
                level = lo
            else:
                level = brentq(lambda cap, want=want: ai_only(cap) - want, lo, hi)
            self.levels[name] = float(max(level, self.params.progress_at_aa) if needs_ac else level)
            self.milestones.pop(name, None)  # AIFM's own date no longer applies

    def class_sds(self, cap: float) -> np.ndarray:
        return np.array([c["level"] + c["slope"] * (cap - c["at"]) for c in self.classes])

    def class_tastes(self, cap: float) -> tuple[np.ndarray, np.ndarray]:
        """(AI judgment, judgment with people) for each class, at capability `cap`."""
        td = self.params.taste_distribution
        ai = np.asarray(td.get_taste_at_sd(self.class_sds(cap)), dtype=float)
        return ai, np.asarray(self.pr.compute_aggregate_research_taste(ai, td), dtype=float)

    def effort_shares(self, tastes) -> np.ndarray:
        """Share of research effort on each class, given the lab's judgment in each."""
        w = (
            np.array([c["share"] for c in self.classes])
            * np.maximum(np.asarray(tastes, float), 1e-300) ** self.class_r
        )
        return w / w.sum()

    def taste_sd(self, cap: float) -> float:
        """AI research judgment in standard deviations of the lab's researchers. With task
        classes, the level that matches the judgment of an AI-only lab."""
        p = self.params
        if self.classes:
            ai = power_mean(
                self.class_tastes(cap)[0], [c["share"] for c in self.classes], self.class_r
            )
            return float(p.taste_distribution.get_sd_of_taste(float(ai)))
        return float(
            p.ai_research_taste_slope * (cap - p.progress_at_aa)
            + p.ai_research_taste_at_coding_automation_anchor_sd
        )

    def people_share(self, cap: float) -> float:
        """Share of researchers whose research judgment is better than the AI's. With task
        classes, better in at least one class."""
        sd = float(self.class_sds(cap).min()) if self.classes else self.taste_sd(cap)
        return 0.5 * math.erfc(sd / math.sqrt(2.0))

    def needs_a_person(self, cap: float) -> float:
        """Share of work that cannot run unsupervised because it turns on a judgment call the
        AI gets wrong. It starts at the share the labs measure on their shortest tasks and
        falls in step with the share of researchers whose judgment is still better than the
        AI's, on fuzzy tasks where there are task classes."""
        if self.residue <= 0.0:
            return 0.0
        today = self.people_share(self.capability_at(self.t_ref))
        return self.residue * min(1.0, self.people_share(cap) / today)

    # ---- calibrated history ----------------------------------------------
    def capability_at(self, date: float) -> float:
        return float(np.interp(date, self.base["t"], self.base["progress"]))

    def base_pace(self, date: float) -> float:
        return float(np.interp(date, self.base["t"], self.base["rate"])) / self.rate0

    def fit_supervision(self, kind: str, cal: dict, **kw) -> None:
        uplift_ref = float(np.interp(self.t_ref, self.base["t"], self.base["coding_mult"]))
        self.supervision = fit_supervision(
            kind, self.capability_at, self.capability_at(self.t_ref), uplift_ref, cal, **kw
        )

    # ---- one evaluation of the right-hand side ---------------------------
    def _inputs(self, t: float, pol: Policy):
        d = self.data
        look = t
        if pol.compute_freeze and t >= pol.start:
            look = pol.start
        H = math.exp(np.interp(t, d.time, d.log_L_HUMAN))
        C = math.exp(np.interp(look, d.time, d.log_inference_H100e))
        X = math.exp(np.interp(look, d.time, d.log_experiment_H100e))
        X_unpaced = math.exp(np.interp(t, d.time, d.log_experiment_H100e))
        tc = np.interp(look, d.time, d.log10_training_H100e) + math.log10(
            self.cfg.FLOP_PER_H100E_YEAR
        )
        if pol.compute_cut != 1.0 and t >= pol.start:
            C, X = C / pol.compute_cut, X / pol.compute_cut
            tc -= math.log10(pol.compute_cut)
        return H, C, X, X_unpaced, tc

    def rhs(
        self,
        t: float,
        logE: float,
        RS: float,
        cap: float,
        pol: Policy,
        supervised: bool,
        cap_start: float | None,
    ):
        p, pr = self.params, self.pr
        H, C, X, X_unpaced, tc = self._inputs(t, pol)
        shares = None
        if self.classes:
            shares = [c["share"] for c in self.classes]
            ai_k, people_k = self.class_tastes(cap)
            taste_ai = float(power_mean(ai_k, shares, self.class_r))
            taste = float(power_mean(people_k, shares, self.class_r))
        else:
            taste_ai = float(pr.compute_ai_research_taste(cap, p))
            taste = pr.compute_aggregate_research_taste(taste_ai, p.taste_distribution)
            ai_k, people_k = taste_ai, taste
        L_opt = p.automation_model.coding_labor_optimal_ces(
            H, C, float(math.log(self.cfg.BASE_FOR_SOFTWARE_LOM) * cap), p
        )
        coding = float(L_opt**p.parallel_penalty * p.coding_labor_normalization)
        human = float(
            self._human_labor(
                None,
                C,
                H,
                p.rho_coding_labor,
                p.parallel_penalty,
                p.coding_labor_normalization,
                human_only=True,
            )
        )
        mult = coding / human  # serial coding labor multiplier
        tau = 1.0 / mult
        if supervised and self.supervision.kind != "none":
            ceiling = 1.0 - self.needs_a_person(cap) if self.residue > 0.0 else None
            tau = max(tau, self.supervision.h(cap, ceiling))
        effort_human = float(
            pr.compute_research_effort(
                X_unpaced,
                human,
                p.alpha_experiment_capacity,
                p.rho_experiment_capacity,
                p.experiment_compute_exponent,
                1.0,
            )
        )

        def effort_of_labor(labor):
            labor = np.asarray(labor, float)
            return (
                np.asarray(
                    pr.compute_research_effort(
                        np.full_like(labor, X),
                        human * labor,
                        p.alpha_experiment_capacity,
                        p.rho_experiment_capacity,
                        p.experiment_compute_exponent,
                        taste,
                    )
                )
                / effort_human
            )

        active = t >= pol.start
        free_labor = 1.0 / tau
        F_free = float(effort_of_labor(np.array([free_labor]))[0])
        spec = pol.gate if (active and pol.gate is not None) else None
        understood, understood_lab, taste_used = 1.0, float("nan"), taste
        if self.link is not None:
            # Measured labor uplift already includes the time people spend understanding
            # what they deploy today, so directing alone is that much more productive.
            out = lab_choice(
                tau * (1.0 - self.link.time_today),
                lambda labor: effort_of_labor(labor) / taste,
                self.labor_ref,
                self.changes,
                spec,
                people_k,
                ai_k,
                self.link,
                spec.hours_multiplier(cap, cap_start) if spec is not None else 1.0,
                self.people_share(cap),
                shares,
                self.class_r,
            )
            F, theta, labor, kept = out["effort"], out["theta"], out["labor"], out["kept"]
            comp, deployed, experiments = (
                out["comprehension_share"],
                out["deployed"],
                out["experiments"],
            )
            understood, understood_lab, taste_used = (
                out["understood"],
                out["understood_lab"],
                out["taste"],
            )
        elif spec is not None:
            out = gate(
                tau, effort_of_labor, self.labor_ref, spec, spec.hours_multiplier(cap, cap_start)
            )
            F, theta, labor, kept = out["effort"], out["theta"], out["labor"], out["kept"]
            comp, deployed, experiments = (
                out["comprehension_share"],
                out["deployed"],
                out["experiments"],
            )
        else:
            F, theta, labor, kept, comp = F_free, 1.0, free_labor, 1.0, 0.0
            deployed = experiments = float("nan")
            if self.changes is not None:
                d = free_deployment(self.changes, labor, self.labor_ref)
                deployed, experiments = d["deployed"], d["experiments"]
                comp = d["hours_if_understood"] / self.changes.hours_per_year
        RE = effort_human * F
        se = p.r_software * math.log10(max(RS, 1e-300) / self.RS_0)
        dlogE = 10.0 ** (tc + se - logE) / math.log(10.0)
        return (
            dlogE,
            RE,
            dict(
                rd_uplift=F,
                labor=labor,
                coding_mult=mult,
                tau=tau,
                theta=theta,
                kept=kept,
                taste=taste_used,
                taste_people=taste,
                taste_ai=taste_ai,
                understood=understood,
                understood_lab=understood_lab,
                rd_free=F_free,
                comprehension_share=comp,
                deployed=deployed,
                experiments=experiments,
            ),
        )

    # ---- forward integration from the reference date ---------------------
    def simulate(
        self,
        policy: Policy | None = None,
        t_end: float = 2032.0,
        supervised: bool = True,
        max_pace: float = 1e6,
        step: float = 0.004,
        stop_after_asi: float = 1.0,
        stop_at: str | None = None,
    ) -> dict:
        """Integrate from t_ref. Stops at t_end, when pace passes max_pace, or once
        progress is `stop_after_asi` orders of magnitude past AIFM's ASI level. With
        `stop_at` naming a milestone, stops just past that milestone instead."""
        pol = policy or Policy()
        b = self.base
        t = self.t_ref
        logE = float(np.interp(t, b["t"], b["progress"]))
        RS = float(np.exp(np.interp(t, b["t"], np.log(b["RS"]))))
        keep = b["t"] < t
        hist_t, hist_E = list(b["t"][keep]), list(b["progress"][keep])
        rows, cap_start = [], None
        ceiling = max(self.levels.values(), default=math.inf) + stop_after_asi
        if stop_at is not None and stop_at in self.levels:
            ceiling = self.levels[stop_at] + 0.02

        def cap_for(time, level):
            if time >= pol.start and pol.lag > 0.0:
                return float(np.interp(time - pol.lag, hist_t + [time], hist_E + [level]))
            return level

        while t < t_end:
            if t >= pol.start and cap_start is None:
                cap_start = logE
            d1, r1, info = self.rhs(t, logE, RS, cap_for(t, logE), pol, supervised, cap_start)
            pace = d1 / self.rate0
            rows.append(
                (
                    t,
                    logE,
                    pace,
                    info["rd_uplift"],
                    info["labor"],
                    info["coding_mult"],
                    info["tau"],
                    info["theta"],
                    info["kept"],
                    info["rd_free"],
                    info["comprehension_share"],
                    info["deployed"],
                    info["experiments"],
                    info["understood"],
                    info["taste"],
                    info["taste_people"],
                    info["taste_ai"],
                    info["understood_lab"],
                )
            )
            if pace > max_pace or logE > ceiling:
                break
            dt = min(step, step / max(pace, 1e-9))
            # Heun's method
            d2, r2, _ = self.rhs(
                t + dt,
                logE + d1 * dt,
                RS + r1 * dt,
                cap_for(t + dt, logE + d1 * dt),
                pol,
                supervised,
                cap_start,
            )
            hist_t.append(t)
            hist_E.append(logE)
            logE += 0.5 * (d1 + d2) * dt
            RS += 0.5 * (r1 + r2) * dt
            t += dt
        cols = [
            "t",
            "progress",
            "pace",
            "rd_uplift",
            "labor",
            "coding_mult",
            "tau",
            "theta",
            "kept",
            "rd_free",
            "comprehension_share",
            "deployed",
            "experiments",
            "understood",
            "taste",
            "taste_people",
            "taste_ai",
            "understood_lab",
        ]
        out = {c: np.array([r[i] for r in rows]) for i, c in enumerate(cols)}
        out["policy"] = pol
        out["stopped_on_pace"] = bool(out["pace"][-1] > max_pace)
        out["ran_away"] = bool(out["stopped_on_pace"] or out["progress"][-1] > ceiling)
        return out

    def summarize(self, run: dict) -> dict:
        t = run["t"]
        s = {
            "pace_2027.5": value_at(t, run["pace"], 2027.5),
            "pace_2028.0": value_at(t, run["pace"], 2028.0),
            "labor_uplift_2028.0": value_at(t, run["labor"], 2028.0),
            "t_pace_3x": first_crossing(t, run["pace"], 3.0),
            "t_pace_10x": first_crossing(t, run["pace"], 10.0),
            "min_kept": float(run["kept"].min()),
            "ran_away": run["ran_away"],
        }
        for name, level in self.levels.items():
            when = first_crossing(t, run["progress"], level)
            if when != when and run.get("stopped_on_pace"):
                when = float(t[-1])  # at a pace past the cap the rest takes hours
            s[f"t_{name.lower().replace('-', '_')}"] = when
        return s


def conditioned_on_pace(
    target: float,
    t_ref: float = 2026.83,
    base: dict | None = None,
    aifm_path: Path | str = DEFAULT_AIFM_PATH,
) -> tuple[Aifm, dict]:
    """Tune the uplift doubling time so AIFM's pace on t_ref equals `target`."""
    from scipy.optimize import brentq

    base = dict(METR_CONDITIONED if base is None else base)

    def miss(months):
        try:
            m = Aifm(dict(base, excess_uplift_doubling_time=months), aifm_path, t_ref)
        except ValueError:  # AIFM cannot fit a schedule this steep
            return 10.0
        return m.base_pace(t_ref) - target

    months = brentq(miss, 2.0, 12.0, xtol=1e-3)
    overrides = dict(base, excess_uplift_doubling_time=float(months))
    return Aifm(overrides, aifm_path, t_ref), overrides
