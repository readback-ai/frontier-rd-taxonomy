.PHONY: setup check lint test validate reports format

# Install Python and every dependency into .venv, exactly as pinned in uv.lock.
setup:
	uv sync

# Lint, tests, record validation and report freshness: the one command CI runs.
check: lint test validate reports

lint:
	uv run ruff check .
	uv run ruff format --check .

test:
	uv run pytest

# Schema, references, verified quotes and coverage rules over data/.
validate:
	uv run taxo validate

# Regenerate reports/ and fail if the committed copies differ from what the records produce.
reports:
	uv run taxo report
	git diff --exit-code -- reports

# Fix what the linter can fix and reformat the code.
format:
	uv run ruff check --fix .
	uv run ruff format .
