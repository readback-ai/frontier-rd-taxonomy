"""Record types. One class per kind of YAML record under ``data/``.

The codebook (docs/codebook.md) defines every scale and category named here, with worked
examples. A value the codebook does not define does not belong in a record.
"""

from __future__ import annotations

import datetime as dt
import re
from typing import Annotated, Literal

from pydantic import BaseModel, ConfigDict, Field, field_validator, model_validator

# --------------------------------------------------------------------------
# Shared pieces
# --------------------------------------------------------------------------
_PERIOD = re.compile(r"^\d{4}(-\d{2}(-\d{2})?)?$")

SourceId = Annotated[str, Field(pattern=r"^S-[a-z0-9]+(-[a-z0-9]+)*$")]
EvidenceId = Annotated[str, Field(pattern=r"^EV-[a-z0-9]+(-[a-z0-9]+)*-\d{2}$")]
TaskId = Annotated[str, Field(pattern=r"^T-[a-z0-9]+(-[a-z0-9]+)*$")]
EstimateId = Annotated[str, Field(pattern=r"^EST-[a-z0-9]+(-[a-z0-9]+)*$")]
RiskId = Annotated[str, Field(pattern=r"^R-[a-z0-9]+(-[a-z0-9]+)*$")]
QuestionId = Annotated[str, Field(pattern=r"^Q-[a-z0-9]+(-[a-z0-9]+)*-\d{2}$")]
IncidentId = Annotated[str, Field(pattern=r"^INC-\d{4}-[a-z0-9]+(-[a-z0-9]+)*$")]
InterventionId = Annotated[str, Field(pattern=r"^IV-[a-z0-9]+(-[a-z0-9]+)*$")]
CrosswalkId = Annotated[str, Field(pattern=r"^XW-[a-z0-9]+(-[a-z0-9]+)*$")]

Text = Annotated[str, Field(min_length=1)]


def _period(value: object) -> str:
    """A year, year-month or full date as text. YAML reads bare dates and years as objects."""
    if isinstance(value, dt.date):
        return value.isoformat()
    text = str(value)
    if not _PERIOD.match(text):
        raise ValueError(f"{text!r} is not YYYY, YYYY-MM or YYYY-MM-DD")
    return text


class Record(BaseModel):
    model_config = ConfigDict(extra="forbid", frozen=True)


# --------------------------------------------------------------------------
# Sources and evidence
# --------------------------------------------------------------------------
SourceType = Literal[
    "incident_report",
    "risk_report",
    "system_card",
    "third_party_investigation",
    "lab_measurement_report",
    "lab_research_post",
    "staff_statement",
    "press_report",
    "academic_paper",
    "forecast_or_model",
    "standard_or_policy",
    "open_source_analog",
    "readback_internal",
]
Vantage = Literal["first_party", "embedded_third_party", "external_third_party", "secondary"]
EvidenceKind = Literal[
    "automation",
    "oversight",
    "comprehension",
    "incident",
    "share",
    "practice",
    "risk",
    "method",
    "pace",
]
Strength = Literal["measured", "reported", "anecdote", "inferred"]
Grade = Literal["A", "B", "C", "D"]

# The best grade a source type can carry (codebook section 3). Analog evidence about public
# repositories lags frontier practice, so it never grades above D.
GRADE_CEILING: dict[str, str] = {
    "incident_report": "A",
    "risk_report": "A",
    "system_card": "A",
    "third_party_investigation": "A",
    "lab_measurement_report": "A",
    "lab_research_post": "B",
    "academic_paper": "B",
    "standard_or_policy": "B",
    "staff_statement": "C",
    "press_report": "C",
    "forecast_or_model": "C",
    "readback_internal": "C",
    "open_source_analog": "D",
}


class Evidence(Record):
    """One claim a source makes, with the words it makes it in."""

    id: EvidenceId
    claim: Text
    quote: Text
    locator: str | None = None
    kind: EvidenceKind
    strength: Strength
    grade: Grade
    tasks: list[TaskId] = []
    describes: str | None = None  # the period the claim is about, if not the publication date
    unverified_reason: str | None = None
    note: str | None = None

    _describes = field_validator("describes", mode="before")(
        lambda v: None if v is None else _period(v)
    )


class Source(Record):
    id: SourceId
    title: Text
    publisher: Text
    authors: list[str] = []
    published: str
    url: Text
    type: SourceType
    vantage: Vantage
    labs: list[str] = []
    summary: Text
    limits: str | None = None
    evidence: list[Evidence] = []

    _published = field_validator("published", mode="before")(_period)

    @model_validator(mode="after")
    def _check(self) -> Source:
        prefix = "EV-" + self.id.removeprefix("S-") + "-"
        ceiling = GRADE_CEILING[self.type]
        for item in self.evidence:
            if not item.id.startswith(prefix):
                raise ValueError(f"{item.id}: evidence ids of {self.id} must start with {prefix}")
            if item.grade < ceiling:
                raise ValueError(
                    f"{item.id}: grade {item.grade} is above the ceiling {ceiling} "
                    f"for a {self.type}"
                )
            if item.grade == "A" and item.strength != "measured":
                raise ValueError(f"{item.id}: grade A needs strength 'measured'")
        return self


# --------------------------------------------------------------------------
# Tasks
# --------------------------------------------------------------------------
OutputRole = Literal["shapes", "measures", "contains", "runs", "decides"]
Verifiability = Literal["mechanical", "empirical", "judgment", "deferred"]
FeedbackLatency = Literal["minutes", "hours", "days", "weeks", "months", "never"]
FailureVisibility = Literal["loud", "quiet", "silent"]
Reversibility = Literal["cheap", "costly", "irreversible"]
Privilege = Literal[
    "none", "internal_code", "training_infra", "eval_infra", "weights", "production", "security"
]
ChangeType = Literal[
    "training_improvement",
    "dataset_update",
    "system_software_change",
    "monitor_change",
    "evaluation_change",
    "decision",
    "none",
]
BranchStatus = Literal["draft", "researched"]


class Task(Record):
    """A node in the task tree. Leaves carry the attributes that drive risk."""

    id: TaskId
    name: Text
    parent: TaskId | None = None
    description: Text
    contributions: list[str] = []  # examples of contributions this task produces
    output_roles: list[OutputRole] = []
    verifiability: Verifiability | None = None
    feedback_latency: FeedbackLatency | None = None
    failure_visibility: FailureVisibility | None = None
    reversibility: Reversibility | None = None
    privilege: list[Privilege] = []
    change_type: ChangeType | None = None
    rationale: str | None = None  # why the attributes are what they are

    @property
    def has_attributes(self) -> bool:
        return bool(
            self.output_roles
            and self.verifiability
            and self.feedback_latency
            and self.failure_visibility
            and self.reversibility
            and self.privilege
            and self.change_type
        )


class TaskFile(Record):
    """One level-1 branch of the tree: the branch node and everything under it."""

    branch: TaskId
    status: BranchStatus = "draft"
    tasks: list[Task]


# --------------------------------------------------------------------------
# Estimates
# --------------------------------------------------------------------------
AutomationLevel = Literal["AL0", "AL1", "AL2", "AL3", "AL4", "AL5"]
ComprehensionLevel = Literal["CL0", "CL1", "CL2", "CL3", "CL4", "CL5"]
OversightMode = Literal[
    "human_every_change",
    "human_sampled",
    "ai_review_human_by_exception",
    "ai_review_only",
    "none",
]
Quantity = Literal[
    "automation_level",
    "comprehension_level",
    "oversight_mode",
    "labor_share",
    "compute_share",
    "advance_share",
    "changes_per_researcher_year",
    "hours_to_understand",
    "elasticity_to_ai_labor",
    "human_review_coverage",
]
LEVEL_QUANTITIES = {"automation_level": "AL", "comprehension_level": "CL"}
SHARE_QUANTITIES = {"labor_share", "compute_share", "advance_share", "human_review_coverage"}
NUMERIC_QUANTITIES = SHARE_QUANTITIES | {
    "changes_per_researcher_year",
    "hours_to_understand",
    "elasticity_to_ai_labor",
}


class LevelValue(Record):
    kind: Literal["level"]
    level: AutomationLevel | ComprehensionLevel


class LevelsValue(Record):
    """Shares of the task's work at each level. Shares sum to 1."""

    kind: Literal["levels"]
    shares: dict[AutomationLevel | ComprehensionLevel, float]

    @model_validator(mode="after")
    def _check(self) -> LevelsValue:
        if any(share < 0 for share in self.shares.values()):
            raise ValueError("shares must not be negative")
        total = sum(self.shares.values())
        if abs(total - 1.0) > 0.011:
            raise ValueError(f"shares sum to {total:.3f}, not 1")
        if len({level[:2] for level in self.shares}) > 1:
            raise ValueError("shares mix automation and comprehension levels")
        return self


class RangeValue(Record):
    """A number with an 80% interval: low is the 10th percentile, high the 90th."""

    kind: Literal["range"]
    low: float
    central: float
    high: float

    @model_validator(mode="after")
    def _check(self) -> RangeValue:
        if not self.low <= self.central <= self.high:
            raise ValueError("need low <= central <= high")
        return self


class PointValue(Record):
    """A number a source states outright, with no interval of ours added."""

    kind: Literal["point"]
    value: float


class CategoryValue(Record):
    kind: Literal["category"]
    value: OversightMode


EstimateValue = Annotated[
    LevelValue | LevelsValue | RangeValue | PointValue | CategoryValue,
    Field(discriminator="kind"),
]
Basis = Literal["evidence", "mixed", "judgment"]


class Estimate(Record):
    """Our reading of one quantity for one task, at one time, for one organization or all."""

    id: EstimateId
    task: TaskId
    quantity: Quantity
    scope: Text  # an organization's name, or "frontier" for the leading labs together
    as_of: str
    value: EstimateValue
    denominator: str | None = None  # for shares: what the share is a share of
    basis: Basis
    evidence: list[EvidenceId] = []
    reasoning: Text
    confidence: Literal["low", "medium", "high"]
    stale_after: dt.date

    _as_of = field_validator("as_of", mode="before")(_period)

    @model_validator(mode="after")
    def _check(self) -> Estimate:
        if self.basis in ("evidence", "mixed") and not self.evidence:
            raise ValueError(f"{self.id}: basis '{self.basis}' needs at least one evidence id")
        if self.basis == "judgment" and self.confidence == "high":
            raise ValueError(f"{self.id}: a judgment-only estimate cannot be high confidence")
        kind = self.value.kind
        prefix = LEVEL_QUANTITIES.get(self.quantity)
        if prefix:
            if kind not in ("level", "levels"):
                raise ValueError(f"{self.id}: {self.quantity} needs a level or levels value")
            levels = [self.value.level] if kind == "level" else list(self.value.shares)
            if any(not level.startswith(prefix) for level in levels):
                raise ValueError(f"{self.id}: {self.quantity} takes {prefix} levels")
        elif self.quantity == "oversight_mode":
            if kind != "category":
                raise ValueError(f"{self.id}: oversight_mode needs a category value")
        elif kind not in ("range", "point"):
            raise ValueError(f"{self.id}: {self.quantity} needs a range or point value")
        if self.quantity in SHARE_QUANTITIES:
            if not self.denominator:
                raise ValueError(f"{self.id}: a share needs a denominator")
            numbers = (
                [self.value.value]
                if kind == "point"
                else [self.value.low, self.value.central, self.value.high]
            )
            if any(not 0.0 <= number <= 1.0 for number in numbers):
                raise ValueError(f"{self.id}: a share must be between 0 and 1")
        return self


class EstimateFile(Record):
    task: TaskId
    estimates: list[Estimate]

    @model_validator(mode="after")
    def _check(self) -> EstimateFile:
        for estimate in self.estimates:
            if estimate.task != self.task:
                raise ValueError(f"{estimate.id}: task {estimate.task} is not {self.task}")
        return self


# --------------------------------------------------------------------------
# Risks
# --------------------------------------------------------------------------
HarmPath = Literal[
    "false_assurance",
    "model_misshaped",
    "containment_weakened",
    "oversight_outpaced",
    "capacity_degraded",
]
Mechanism = Literal[
    "comprehension_gap",
    "review_overload",
    "correlated_error",
    "adversarial_model",
    "accountability_diffusion",
    "spec_gap",
    "skill_atrophy",
    "time_pressure",
]
RiskStatus = Literal["hypothesized", "observed_analog", "observed_frontier"]


class Risk(Record):
    id: RiskId
    title: Text
    tasks: list[TaskId] = Field(min_length=1)
    failure_mode: Text
    harm_path: HarmPath
    mechanisms: list[Mechanism] = Field(min_length=1)
    automation_effect: Text
    review_catchable: Literal["yes", "partly", "no"]
    review_rationale: Text
    severity: Literal["low", "moderate", "high", "critical"]
    status: RiskStatus
    evidence: list[EvidenceId] = []
    incidents: list[IncidentId] = []

    @model_validator(mode="after")
    def _check(self) -> Risk:
        if self.status != "hypothesized" and not (self.evidence or self.incidents):
            raise ValueError(f"{self.id}: status '{self.status}' needs evidence or an incident")
        return self


# --------------------------------------------------------------------------
# Review questions
# --------------------------------------------------------------------------
QuestionCategory = Literal["what", "why", "failure", "dependency", "side_effects", "provenance"]
TopicalArea = Literal[
    "architecture_design",
    "implementation_behavior",
    "process",
    "key_findings",
    "analysis_of_results",
]
# The audit paper's tiers of required understanding (Table 1), by topical area (Table 4).
TIER_OF_AREA: dict[str, str] = {
    "architecture_design": "deep",
    "implementation_behavior": "deep",
    "process": "deep",
    "key_findings": "familiarity",
    "analysis_of_results": "familiarity",
}


class Question(Record):
    id: QuestionId
    category: QuestionCategory
    topical_area: TopicalArea
    question: Text
    good_answer_shows: Text
    red_flags: list[Text] = Field(min_length=1)
    evidence_to_request: str | None = None
    risks: list[RiskId] = []

    @property
    def tier(self) -> str:
        return TIER_OF_AREA[self.topical_area]


class QuestionSet(Record):
    """Questions a reviewer brings to a contribution of this kind."""

    task: TaskId
    contribution: Text  # the kind of contribution under review
    questions: list[Question] = Field(min_length=1)


# --------------------------------------------------------------------------
# Incidents
# --------------------------------------------------------------------------
class Backtest(Record):
    question: QuestionId
    verdict: Literal["would_surface", "might_surface", "would_not_surface"]
    rationale: Text


class Incident(Record):
    id: IncidentId
    title: Text
    org: Text
    frontier: bool  # a frontier lab's own work, as opposed to an analog elsewhere
    occurred: str
    disclosed: str | None = None
    summary: Text
    root_cause: Text
    detected_by: Text
    detection_latency: str | None = None
    automation_involved: Literal["yes", "no", "unknown"]
    comprehension_failure: Literal["yes", "partly", "no", "unknown"]
    comprehension_note: Text
    tasks: list[TaskId] = Field(min_length=1)
    risks: list[RiskId] = []
    evidence: list[EvidenceId] = Field(min_length=1)
    backtest: list[Backtest] = []

    _occurred = field_validator("occurred", mode="before")(_period)
    _disclosed = field_validator("disclosed", mode="before")(
        lambda v: None if v is None else _period(v)
    )


# --------------------------------------------------------------------------
# Interventions and crosswalks
# --------------------------------------------------------------------------
InterventionKind = Literal[
    "comprehension_gate",
    "signoff_gate",
    "internal_use_lag",
    "compute_limit",
    "review_tooling",
    "reviewer_supply",
    "automation_cap",
    "independent_audit",
]


class Targets(Record):
    tasks: list[TaskId] = []
    output_roles: list[OutputRole] = []
    change_types: list[ChangeType] = []


class Intervention(Record):
    id: InterventionId
    name: Text
    kind: InterventionKind
    description: Text
    targets: Targets = Targets()
    pacing_policy: str | None = None  # the policy's name in the readback-ops pacing model
    hours_scale: float | None = None  # multiplies hours_to_understand on targeted changes
    evidence: list[EvidenceId] = []
    note: str | None = None


class CrosswalkEntry(Record):
    external_id: Text
    external_label: Text
    tasks: list[TaskId] = []
    note: str | None = None


class Crosswalk(Record):
    """How another taxonomy's categories map onto task ids here."""

    id: CrosswalkId
    name: Text
    source: SourceId | None = None
    description: Text
    entries: list[CrosswalkEntry]
