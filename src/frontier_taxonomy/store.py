"""Load every record under ``data/`` into one in-memory dataset."""

from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path

import yaml
from pydantic import ValidationError

from .config import Paths
from .schema import (
    Crosswalk,
    Estimate,
    EstimateFile,
    Evidence,
    Incident,
    Intervention,
    Question,
    QuestionSet,
    Record,
    Risk,
    Source,
    Task,
    TaskFile,
)


@dataclass(frozen=True)
class Problem:
    level: str  # "error" or "warning"
    where: str
    message: str


@dataclass
class Dataset:
    sources: dict[str, Source] = field(default_factory=dict)
    evidence: dict[str, Evidence] = field(default_factory=dict)
    evidence_source: dict[str, str] = field(default_factory=dict)  # evidence id -> source id
    tasks: dict[str, Task] = field(default_factory=dict)
    branches: dict[str, TaskFile] = field(default_factory=dict)
    estimates: dict[str, Estimate] = field(default_factory=dict)
    risks: dict[str, Risk] = field(default_factory=dict)
    question_sets: dict[str, QuestionSet] = field(default_factory=dict)  # by task id
    questions: dict[str, Question] = field(default_factory=dict)
    question_task: dict[str, str] = field(default_factory=dict)  # question id -> task id
    incidents: dict[str, Incident] = field(default_factory=dict)
    interventions: dict[str, Intervention] = field(default_factory=dict)
    crosswalks: dict[str, Crosswalk] = field(default_factory=dict)

    # ---- tree helpers ----------------------------------------------------
    def children(self, task_id: str) -> list[Task]:
        return [task for task in self.tasks.values() if task.parent == task_id]

    def is_leaf(self, task_id: str) -> bool:
        return not self.children(task_id)

    def ancestors(self, task_id: str) -> list[str]:
        """Parent, grandparent and so on up to the branch. Stops if it meets a cycle."""
        chain: list[str] = []
        current = self.tasks.get(task_id)
        while current and current.parent and current.parent not in chain:
            chain.append(current.parent)
            current = self.tasks.get(current.parent)
        return chain

    def branch_of(self, task_id: str) -> str:
        chain = self.ancestors(task_id)
        return chain[-1] if chain else task_id

    def descendants(self, task_id: str) -> list[Task]:
        found: list[Task] = []
        frontier = [task_id]
        seen = {task_id}
        while frontier:
            for child in self.children(frontier.pop()):
                if child.id not in seen:
                    seen.add(child.id)
                    found.append(child)
                    frontier.append(child.id)
        return found

    def depth(self, task_id: str) -> int:
        return len(self.ancestors(task_id)) + 1

    def change_types_under(self, task_id: str) -> set[str]:
        """The change types deployed by a task or by any task below it."""
        tasks = [self.tasks[task_id], *self.descendants(task_id)] if task_id in self.tasks else []
        return {t.change_type for t in tasks if t.change_type and t.change_type != "none"}

    def change_type_of(self, estimate: Estimate) -> str | None:
        """The change type a gate estimate is about: its own, or its leaf task's."""
        if estimate.change_type:
            return estimate.change_type
        task = self.tasks.get(estimate.task)
        if task and task.change_type and task.change_type != "none":
            return task.change_type
        return None


_FOLDERS: dict[str, type[Record]] = {
    "sources": Source,
    "tasks": TaskFile,
    "estimates": EstimateFile,
    "risks": Risk,
    "questions": QuestionSet,
    "incidents": Incident,
    "interventions": Intervention,
    "crosswalks": Crosswalk,
}


def _read_yaml(path: Path) -> object:
    with open(path, encoding="utf-8") as handle:
        return yaml.safe_load(handle)


def _short(error: ValidationError) -> str:
    parts = []
    for item in error.errors():
        location = ".".join(str(piece) for piece in item["loc"])
        parts.append(f"{location}: {item['msg']}" if location else item["msg"])
    return "; ".join(parts)


def load(paths: Paths, problems: list[Problem] | None = None) -> Dataset:
    """Every record under ``data/``. Unreadable or invalid files become problems.

    With ``problems`` left as None, the first invalid file raises ``ValueError``.
    """
    collected: list[Problem] = [] if problems is None else problems
    dataset = Dataset()

    def problem(where: str, message: str) -> None:
        if problems is None:
            raise ValueError(f"{where}: {message}")
        collected.append(Problem("error", where, message))

    def add(table: dict, key: str, value: object, where: str) -> None:
        if key in table:
            problem(where, f"duplicate id {key}")
        table[key] = value

    for folder, model in _FOLDERS.items():
        for path in sorted((paths.records / folder).glob("*.yml")):
            where = str(path.relative_to(paths.root))
            try:
                record = model.model_validate(_read_yaml(path))
            except ValidationError as error:
                problem(where, _short(error))
                continue
            except (yaml.YAMLError, OSError) as error:
                problem(where, f"unreadable: {error}")
                continue

            stem = path.stem
            if isinstance(record, Source):
                if record.id != stem:
                    problem(where, f"file name must be {record.id}.yml")
                add(dataset.sources, record.id, record, where)
                for item in record.evidence:
                    add(dataset.evidence, item.id, item, where)
                    dataset.evidence_source[item.id] = record.id
            elif isinstance(record, TaskFile):
                if record.branch != stem:
                    problem(where, f"file name must be {record.branch}.yml")
                add(dataset.branches, record.branch, record, where)
                for task in record.tasks:
                    add(dataset.tasks, task.id, task, where)
            elif isinstance(record, EstimateFile):
                if record.task != stem:
                    problem(where, f"file name must be {record.task}.yml")
                for estimate in record.estimates:
                    add(dataset.estimates, estimate.id, estimate, where)
            elif isinstance(record, QuestionSet):
                if record.task != stem:
                    problem(where, f"file name must be {record.task}.yml")
                add(dataset.question_sets, record.task, record, where)
                for question in record.questions:
                    add(dataset.questions, question.id, question, where)
                    dataset.question_task[question.id] = record.task
            else:
                table = getattr(dataset, folder)
                if record.id != stem:
                    problem(where, f"file name must be {record.id}.yml")
                add(table, record.id, record, where)
    return dataset


def source_url(paths: Paths, source_id: str) -> str | None:
    """The url in a source's record, read without validating the rest of the dataset."""
    path = paths.records / "sources" / f"{source_id}.yml"
    if not path.is_file():
        return None
    data = _read_yaml(path)
    return data.get("url") if isinstance(data, dict) else None
