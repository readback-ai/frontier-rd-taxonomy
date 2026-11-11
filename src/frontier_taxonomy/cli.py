"""The ``taxo`` command.

taxo snapshot <source-id> [--url URL | --from-file PATH]   fetch and store a source
taxo check-quote <source-id> "<quote>"                      is this text in the snapshot?
taxo verify-quotes [<source-id> ...]                        stamp every verified quote
taxo validate [--strict]                                    schema, references and rules
taxo report                                                 regenerate reports/
taxo gate-inputs                                            pacing-model inputs
taxo stale [--as-of DATE]                                   estimates past their date
"""

from __future__ import annotations

import argparse
import datetime as dt
import sys
from pathlib import Path

from .config import Paths
from .snapshot import SnapshotError, read_snapshot, snapshot_file, snapshot_url
from .textnorm import find_quote, normalize


def _cmd_snapshot(args: argparse.Namespace) -> int:
    from .locks import record_snapshot
    from .store import source_url

    paths = Paths.discover()
    url = args.url or source_url(paths, args.source_id)
    if not url:
        print(
            f"{args.source_id}: no --url given and no record in data/sources/ to read it from",
            file=sys.stderr,
        )
        return 2
    folder = paths.snapshot_dir(args.source_id)
    try:
        if args.from_file:
            meta = snapshot_file(folder, args.source_id, url, Path(args.from_file))
        else:
            meta = snapshot_url(folder, args.source_id, url)
    except SnapshotError as error:
        print(f"snapshot failed: {error}", file=sys.stderr)
        return 1
    # A lock belongs to a source record. A snapshot taken to decide whether a source is worth
    # adding leaves none; `taxo verify-quotes` writes the lock once the record exists.
    if (paths.records / "sources" / f"{args.source_id}.yml").is_file():
        record_snapshot(paths, meta)
    print(f"{args.source_id}: {meta.text_chars} characters, sha256 {meta.text_sha256[:12]}")
    print(f"text: {folder / 'text.txt'}")
    if meta.paywalled:
        print(
            "WARNING: the page marks itself paywalled. The snapshot may hold text a non-subscriber "
            "is not shown. Quote only what the page shows without a subscription."
        )
    return 0


def _cmd_check_quote(args: argparse.Namespace) -> int:
    paths = Paths.discover()
    stored = read_snapshot(paths.snapshot_dir(args.source_id))
    if stored is None:
        print(f"{args.source_id}: no snapshot. Run `taxo snapshot` first.", file=sys.stderr)
        return 2
    _, text = stored
    spans = find_quote(text, args.quote)
    if spans is None:
        print("NOT FOUND: the quote is not in the snapshot text as written.")
        return 1
    haystack = normalize(text)
    start, end = spans[0][0], spans[-1][1]
    context = haystack[max(0, start - 80) : min(len(haystack), end + 80)]
    print(f"FOUND ({len(spans)} segment(s)). Context: ...{context}...")
    return 0


def _cmd_verify_quotes(args: argparse.Namespace) -> int:
    from .verify import verify_quotes

    paths = Paths.discover()
    results = verify_quotes(paths, args.source_ids or None)
    failed = [r for r in results if r.status == "not_found"]
    missing = [r for r in results if r.status == "no_snapshot"]
    invalid = [r for r in results if r.status == "invalid_record"]
    verified = [r for r in results if r.status == "verified"]
    for result in invalid:
        print(f"INVALID RECORD  {result.source_id}: {result.detail}")
    for result in failed:
        print(f"NOT FOUND  {result.evidence_id}")
    for source_id in sorted({r.source_id for r in missing}):
        print(f"NO SNAPSHOT  {source_id}")
    print(
        f"{len(verified)} verified, {len(failed)} not found, "
        f"{len(missing)} without a snapshot, {len(invalid)} invalid record(s)"
    )
    return 1 if failed or invalid else 0


def _cmd_prune_locks(args: argparse.Namespace) -> int:
    paths = Paths.discover()
    sources = {path.stem for path in (paths.records / "sources").glob("*.yml")}
    removed = 0
    for lock_file in sorted(paths.locks.glob("*.json")):
        if lock_file.stem not in sources:
            lock_file.unlink()
            print(f"removed {lock_file.relative_to(paths.root)}")
            removed += 1
    print(f"{removed} lock file(s) with no source record removed")
    return 0


def _cmd_validate(args: argparse.Namespace) -> int:
    from .validate import validate

    paths = Paths.discover()
    problems = validate(paths, as_of=_as_of(args))
    errors = [p for p in problems if p.level == "error"]
    warnings = [p for p in problems if p.level == "warning"]
    for problem in errors + warnings:
        print(f"{problem.level.upper():7}  {problem.where}: {problem.message}")
    print(f"{len(errors)} error(s), {len(warnings)} warning(s)")
    if errors or (args.strict and warnings):
        return 1
    return 0


def _cmd_report(args: argparse.Namespace) -> int:
    from .report import write_reports

    paths = Paths.discover()
    as_of = dt.date.fromisoformat(args.as_of) if args.as_of else None
    for path in write_reports(paths, as_of=as_of):
        print(path.relative_to(paths.root))
    return 0


def _cmd_gate_inputs(args: argparse.Namespace) -> int:
    from .pacing import write_gate_inputs

    paths = Paths.discover()
    print(write_gate_inputs(paths).relative_to(paths.root))
    return 0


def _cmd_pack_snapshots(args: argparse.Namespace) -> int:
    from .archive import pack_snapshots
    from .store import load

    paths = Paths.discover()
    out = Path(args.out)
    packed = pack_snapshots(paths, out, include_raw=not args.text_only)
    absent = sorted(set(load(paths).sources) - set(packed))
    print(f"{out}: {len(packed)} snapshot(s), {out.stat().st_size / 1e6:.1f} MB")
    for source_id in absent:
        print(f"  no snapshot on disk: {source_id}")
    return 0


def _cmd_restore_snapshots(args: argparse.Namespace) -> int:
    from .archive import restore_snapshots

    paths = Paths.discover()
    results = restore_snapshots(paths, Path(args.archive))
    for result in results:
        if result.status != "matches":
            print(f"  {result.status}: {result.source_id}")
    matched = sum(1 for r in results if r.status == "matches")
    print(f"{len(results)} snapshot(s) restored to {paths.snapshots}, {matched} match their lock")
    if matched < len(results):
        print("Run `taxo verify-quotes` for the rest before relying on their quotes.")
    return 0


def _cmd_sensitivity(args: argparse.Namespace) -> int:
    import os

    from .sensitivity import write_sensitivity

    paths = Paths.discover()
    model_dir = args.model_dir or os.environ.get("FRT_PACING_MODEL_DIR")
    if not model_dir:
        print(
            "Name the pacing model's folder with --model-dir or FRT_PACING_MODEL_DIR "
            "(readback-ops/research/pacing-takeoff-model).",
            file=sys.stderr,
        )
        return 2
    try:
        out = write_sensitivity(paths, Path(model_dir), draws=args.draws)
    except ModuleNotFoundError as missing:
        print(
            f"The pacing model needs {missing.name}. Run with the extra: "
            "uv run --extra pacing taxo sensitivity ...",
            file=sys.stderr,
        )
        return 2
    print(out.relative_to(paths.root))
    return 0


def _cmd_stale(args: argparse.Namespace) -> int:
    from .store import load
    from .validate import stale_estimates

    paths = Paths.discover()
    stale = stale_estimates(load(paths), _as_of(args))
    for estimate in stale:
        print(f"{estimate.id}  as of {estimate.as_of}  stale after {estimate.stale_after}")
    print(f"{len(stale)} stale estimate(s)")
    return 0


def _as_of(args: argparse.Namespace) -> dt.date:
    return dt.date.fromisoformat(args.as_of) if getattr(args, "as_of", None) else dt.date.today()


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="taxo", description=__doc__.splitlines()[0])
    sub = parser.add_subparsers(dest="command", required=True)

    snap = sub.add_parser("snapshot", help="fetch a source and store its text")
    snap.add_argument("source_id")
    snap.add_argument("--url", help="defaults to the url in the source's record")
    snap.add_argument("--from-file", help="a copy of the page or PDF that a person saved")
    snap.set_defaults(func=_cmd_snapshot)

    check = sub.add_parser("check-quote", help="check one quote against a snapshot")
    check.add_argument("source_id")
    check.add_argument("quote")
    check.set_defaults(func=_cmd_check_quote)

    verify = sub.add_parser("verify-quotes", help="verify every quote and write lock files")
    verify.add_argument("source_ids", nargs="*")
    verify.set_defaults(func=_cmd_verify_quotes)

    prune = sub.add_parser("prune-locks", help="delete lock files that have no source record")
    prune.set_defaults(func=_cmd_prune_locks)

    val = sub.add_parser("validate", help="check records, references and rules")
    val.add_argument("--strict", action="store_true", help="warnings fail too")
    val.add_argument("--as-of", help="date for staleness checks (default today)")
    val.set_defaults(func=_cmd_validate)

    rep = sub.add_parser("report", help="regenerate reports/")
    rep.add_argument("--as-of", help="report date (default: the latest quote verification)")
    rep.set_defaults(func=_cmd_report)

    gate = sub.add_parser("gate-inputs", help="write pacing-model gate inputs")
    gate.set_defaults(func=_cmd_gate_inputs)

    pack = sub.add_parser("pack-snapshots", help="archive snapshots for storage outside git")
    pack.add_argument("--out", default="snapshots.tar.gz", help="archive to write")
    pack.add_argument("--text-only", action="store_true", help="leave out the raw captures")
    pack.set_defaults(func=_cmd_pack_snapshots)

    restore = sub.add_parser(
        "restore-snapshots", help="unpack an archive and check it against locks"
    )
    restore.add_argument("archive")
    restore.set_defaults(func=_cmd_restore_snapshots)

    sens = sub.add_parser(
        "sensitivity", help="run the readback-ops pacing model on the gate inputs and rank them"
    )
    sens.add_argument("--model-dir", help="readback-ops/research/pacing-takeoff-model")
    sens.add_argument("--draws", type=int, default=150, help="joint draws over the priors")
    sens.set_defaults(func=_cmd_sensitivity)

    stale = sub.add_parser("stale", help="list estimates past their stale-after date")
    stale.add_argument("--as-of")
    stale.set_defaults(func=_cmd_stale)
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    return args.func(args)


if __name__ == "__main__":
    sys.exit(main())
