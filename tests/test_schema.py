import copy
import datetime as dt

import pytest
from conftest import ESTIMATES, RISK, SOURCE, estimate
from pydantic import ValidationError

from frontier_taxonomy.schema import Estimate, EstimateFile, Risk, Source


def source_with(**changes) -> dict:
    record = copy.deepcopy(SOURCE)
    record["evidence"][0].update(changes.pop("first_item", {}))
    record.update(changes)
    return record


def test_valid_records_load():
    source = Source.model_validate(SOURCE)
    assert source.published == "2026-01-15"
    assert len(source.evidence) == 2
    assert len(EstimateFile.model_validate(ESTIMATES).estimates) == 4


def test_yaml_dates_and_years_become_text():
    assert Source.model_validate(source_with(published=dt.date(2026, 1, 15))).published == (
        "2026-01-15"
    )
    assert Source.model_validate(source_with(published=2026)).published == "2026"
    with pytest.raises(ValidationError):
        Source.model_validate(source_with(published="January 2026"))


def test_unknown_fields_are_rejected():
    with pytest.raises(ValidationError):
        Source.model_validate(source_with(reliability="high"))


def test_evidence_ids_carry_their_source():
    with pytest.raises(ValidationError, match="must start with"):
        Source.model_validate(source_with(first_item={"id": "EV-other-source-01"}))


def test_source_type_caps_the_grade():
    analog = source_with(type="open_source_analog")
    with pytest.raises(ValidationError, match="above the ceiling"):
        Source.model_validate(analog)
    for item in analog["evidence"]:
        item["grade"] = "D"
    assert Source.model_validate(analog)


def test_grade_a_needs_a_measurement():
    with pytest.raises(ValidationError, match="grade A needs"):
        Source.model_validate(source_with(first_item={"grade": "A"}))


def test_estimate_needs_evidence_unless_it_says_judgment():
    with pytest.raises(ValidationError, match="needs at least one evidence id"):
        Estimate.model_validate(
            estimate("a", "automation_level", {"kind": "level", "level": "AL3"}, evidence=[])
        )
    assert Estimate.model_validate(
        estimate(
            "a",
            "automation_level",
            {"kind": "level", "level": "AL3"},
            evidence=[],
            basis="judgment",
        )
    )


def test_judgment_cannot_be_high_confidence():
    with pytest.raises(ValidationError, match="cannot be high confidence"):
        Estimate.model_validate(
            estimate(
                "a",
                "automation_level",
                {"kind": "level", "level": "AL3"},
                evidence=[],
                basis="judgment",
                confidence="high",
            )
        )


def test_value_kind_must_fit_the_quantity():
    with pytest.raises(ValidationError, match="needs a level or levels value"):
        Estimate.model_validate(estimate("a", "automation_level", {"kind": "point", "value": 3}))
    with pytest.raises(ValidationError, match="takes AL levels"):
        Estimate.model_validate(
            estimate("a", "automation_level", {"kind": "level", "level": "CL2"})
        )
    with pytest.raises(ValidationError, match="needs a range or point value"):
        Estimate.model_validate(
            estimate("a", "hours_to_understand", {"kind": "level", "level": "AL2"})
        )


def test_level_shares_sum_to_one():
    good = {"kind": "levels", "shares": {"AL3": 0.7, "AL4": 0.3}}
    assert Estimate.model_validate(estimate("a", "automation_level", good))
    bad = {"kind": "levels", "shares": {"AL3": 0.7, "AL4": 0.6}}
    with pytest.raises(ValidationError, match="not 1"):
        Estimate.model_validate(estimate("a", "automation_level", bad))


def test_shares_need_a_denominator_and_stay_in_range():
    value = {"kind": "range", "low": 0.01, "central": 0.03, "high": 0.06}
    with pytest.raises(ValidationError, match="needs a denominator"):
        Estimate.model_validate(estimate("a", "labor_share", value))
    assert Estimate.model_validate(
        estimate("a", "labor_share", value, denominator="all model R&D person-time")
    )
    with pytest.raises(ValidationError, match="between 0 and 1"):
        Estimate.model_validate(
            estimate(
                "a",
                "labor_share",
                {"kind": "point", "value": 6},
                denominator="all model R&D person-time",
            )
        )


def test_range_must_be_ordered():
    with pytest.raises(ValidationError, match="low <= central <= high"):
        Estimate.model_validate(
            estimate(
                "a", "hours_to_understand", {"kind": "range", "low": 9, "central": 5, "high": 7}
            )
        )


def test_observed_risk_needs_something_observed():
    record = dict(RISK, evidence=[], incidents=[])
    with pytest.raises(ValidationError, match="needs evidence or an incident"):
        Risk.model_validate(record)
    assert Risk.model_validate(dict(record, status="hypothesized"))
