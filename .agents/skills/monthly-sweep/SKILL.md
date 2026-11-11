---
name: monthly-sweep
description: Monthly refresh of the taxonomy's evidence. Re-snapshot sources to detect silent edits, find new sources by family, flag stale estimates, and report what changed in the conclusions. Use when asked to run the monthly sweep or update the taxonomy with new information.
---

# Monthly sweep

The aim is a short, reviewable delta: what is new, what moved, what went stale. Work on one branch named `sweep-YYYY-MM` and open one pull request.

## 1. Detect drift in existing sources

For each source record, re-run `uv run taxo snapshot <id>` and then `uv run taxo verify-quotes`.

- A changed hash with every quote still verified: the page changed around our quotes. Nothing to do.
- A quote no longer found: the source was edited. Do not just re-copy. Read what changed. A developer revising a system card or risk report after publication is itself a finding for the claim registry; note it in the pull request with the old quote and the new text.
- A page that now refuses the fetch: leave the lock as it is and list the source as unreachable.

## 2. New sources

Run `sweep-sources` for each family, for documents published since the last sweep (the latest `published` date in `data/sources/` per publisher is the starting point):

1. New system cards, risk reports and incident disclosures from each frontier developer.
2. New third-party assessments (METR, Apollo, AISI, CAISI, Transluce, Epoch, embedded evaluators).
3. Updates to developers' measurement reports: automation index values, oversight metrics, compute shares.
4. New incidents in the branches already researched.

Then run `verify-evidence` on everything added.

## 3. Re-read the estimates the new evidence touches

For each new item, list the estimates on the same task and quantity. If the item contradicts or tightens one, write a new estimate with the new `as_of`; keep the old one. History is the point: the pacing model reads the trend.

Run `uv run taxo stale`. For each stale estimate, either support it with current evidence and a new `as_of`, or leave it stale. Do not move the date on an estimate you did not re-examine.

## 4. Incidents and questions

Add incidents. Run the backtest in `draft-questions` for each new incident against the existing sets. An incident no question would have surfaced goes at the top of the pull request.

## 5. Report

`uv run taxo report` and `make check`. If any gate input changed, run `taxo sensitivity` again (`taxo validate` warns when it is out of date). Pack the snapshots with `uv run taxo pack-snapshots` and put the archive in the organization's snapshot folder (spec decision D15); a session's disk does not last. The pull request carries the readback from `AGENTS.md`, plus:

- Sources added, by type. Sources edited by their publisher since last month.
- Estimates changed: old value, new value, the evidence that moved it.
- Change in the judgment-only share.
- Gate inputs that changed in `reports/gate-inputs.yml`, since the pacing model reads them.
- Searches that found nothing.
