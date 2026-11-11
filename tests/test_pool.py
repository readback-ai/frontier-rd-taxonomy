"""Pooling per-developer estimates into one frontier figure (spec decision D16)."""

from __future__ import annotations

import yaml
from conftest import ESTIMATES, SOURCE, estimate, write_record

from frontier_taxonomy.config import Paths
from frontier_taxonomy.pool import REQUIRED_LABS, canonical_lab, lab_coverage, pool
from frontier_taxonomy.report import coverage_report
from frontier_taxonomy.store import load
from frontier_taxonomy.validate import validate


def with_estimates(paths: Paths, *extra: dict) -> None:
    record = dict(ESTIMATES, estimates=[*ESTIMATES["estimates"], *extra])
    write_record(paths, "estimates/T-x-graders.yml", record)


def lab_level(lab: str, level: str, suffix: str | None = None) -> dict:
    slug = suffix or lab.lower().replace(" ", "-")
    return estimate(
        f"automation-{slug}", "automation_level", {"kind": "level", "level": level}, scope=lab
    )


def test_lab_names_are_canonical():
    assert canonical_lab("Google") == "Google DeepMind"
    assert canonical_lab("GDM") == "Google DeepMind"
    assert canonical_lab("OpenAI") == "OpenAI"
    assert canonical_lab("METR") == "METR"
    assert REQUIRED_LABS == ("Anthropic", "OpenAI", "Google DeepMind")


def test_a_pool_needs_all_three_labs(verified: Paths):
    with_estimates(verified, lab_level("Anthropic", "AL4"), lab_level("Google DeepMind", "AL3"))
    pooled = pool(load(verified), "T-x-graders", "automation_level")
    assert not pooled.complete
    assert pooled.missing == ("OpenAI",)
    assert pooled.text() == "needs OpenAI"

    with_estimates(
        verified,
        lab_level("Anthropic", "AL4"),
        lab_level("Google DeepMind", "AL3"),
        lab_level("OpenAI", "AL3"),
    )
    pooled = pool(load(verified), "T-x-graders", "automation_level")
    assert pooled.complete
    assert pooled.text() == "AL3 to AL4"
    assert pooled.basis == "evidence"


def test_labs_that_agree_pool_to_one_value(verified: Paths):
    with_estimates(verified, *(lab_level(lab, "AL3") for lab in REQUIRED_LABS))
    assert pool(load(verified), "T-x-graders", "automation_level").text() == "AL3"


def test_level_shares_pool_by_their_largest_share(verified: Paths):
    shares = {"kind": "levels", "shares": {"AL2": 0.1, "AL3": 0.6, "AL4": 0.3}}
    with_estimates(
        verified,
        estimate("automation-anthropic", "automation_level", shares, scope="Anthropic"),
        lab_level("OpenAI", "AL4"),
        lab_level("Google DeepMind", "AL4"),
    )
    assert pool(load(verified), "T-x-graders", "automation_level").text() == "AL3 to AL4"


def test_oversight_pools_from_most_to_least_human(verified: Paths):
    def mode(lab: str, value: str) -> dict:
        return estimate(
            f"oversight-{lab.lower().replace(' ', '-')}",
            "oversight_mode",
            {"kind": "category", "value": value},
            scope=lab,
        )

    with_estimates(
        verified,
        mode("Anthropic", "ai_review_human_by_exception"),
        mode("OpenAI", "ai_review_only"),
        mode("Google DeepMind", "human_sampled"),
    )
    pooled = pool(load(verified), "T-x-graders", "oversight_mode")
    assert pooled.text() == "human sampled to ai review only"


def test_numbers_pool_to_the_envelope_and_the_middle_lab(verified: Paths):
    def coverage(lab: str, low: float, central: float, high: float) -> dict:
        return estimate(
            f"coverage-{lab.lower().replace(' ', '-')}",
            "human_review_coverage",
            {"kind": "range", "low": low, "central": central, "high": high},
            scope=lab,
            denominator="transcripts",
        )

    with_estimates(
        verified,
        coverage("Anthropic", 0.003, 0.01, 0.04),
        coverage("OpenAI", 0.01, 0.02, 0.03),
        coverage("Google DeepMind", 0.05, 0.1, 0.2),
    )
    pooled = pool(load(verified), "T-x-graders", "human_review_coverage")
    assert pooled.triple() == (0.003, 0.02, 0.2)


def test_the_latest_estimate_per_lab_is_pooled(verified: Paths):
    with_estimates(
        verified,
        lab_level("Anthropic", "AL2", suffix="anthropic-old") | {"as_of": "2025-06"},
        lab_level("Anthropic", "AL4"),
        lab_level("OpenAI", "AL4"),
        lab_level("Google", "AL4", suffix="gdm"),
    )
    pooled = pool(load(verified), "T-x-graders", "automation_level")
    assert pooled.complete, "Google is Google DeepMind"
    assert pooled.text() == "AL4"


def test_coverage_report_shows_who_is_missing(verified: Paths):
    with_estimates(verified, lab_level("Anthropic", "AL4"), lab_level("Google DeepMind", "AL3"))
    dataset = load(verified)
    assert lab_coverage(dataset, "T-x")["automation_level"] == (0, 1)
    text = coverage_report(verified, dataset, None)
    assert "## Pooled across Anthropic, OpenAI and Google DeepMind" in text
    assert "needs OpenAI" in text
    assert "0 of 2 cells have all three developers" in text


def test_a_frontier_estimate_must_cite_all_three_labs(verified: Paths):
    def warnings() -> list[str]:
        return [p.message for p in validate(verified) if p.level == "warning"]

    assert not any("frontier" in message for message in warnings())
    source = dict(SOURCE, labs=["Anthropic"])
    path = verified.records / "sources" / f"{SOURCE['id']}.yml"
    path.write_text(yaml.safe_dump(source, sort_keys=False), encoding="utf-8")
    found = [message for message in warnings() if "frontier" in message]
    assert found, "an evidence-based frontier estimate resting on one lab is flagged"
    assert "OpenAI" in found[0] and "Google DeepMind" in found[0]
    assert len(found) == 2, "judgment priors are exempt; the two evidence estimates are not"
