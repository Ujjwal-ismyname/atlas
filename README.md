# Atlas

Atlas is a local-first portfolio research and risk-learning application.

It will combine user-provided sample portfolio data with public financial
filings to produce evidence-backed research insights. The project is designed
as an AI engineering apprenticeship: it will progressively introduce
document ingestion, retrieval-augmented generation (RAG), financial tools,
agent workflows, evaluation, observability, security, and deployment.

## Project status

Atlas is in active early development.

- Current milestone: M0 — Portfolio-risk platform foundation
- Current issue: #7 — Configure quality gates: Ruff, Mypy, and Pytest

## Intended users

Atlas is being built for learners and engineers who want to understand how a
production-style AI research system is designed, implemented, tested, and
operated.

## Scope

The first release will support:

- Importing a small sample portfolio
- Retrieving evidence from selected public company filings
- Calculating deterministic portfolio and financial metrics
- Producing cited research summaries

## Non-goals

Atlas is not:

- Investment advice
- A trading or brokerage platform
- A real-time market-data system
- A portfolio execution system
- A replacement for professional financial, legal, or tax advice

## Local development

### Prerequisites

- Python 3.12 or newer

### Setup

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install -e ".[dev]"
```

### Quality gates

Run the automated checks locally before committing:

```bash
# Format check & linting
ruff check .
ruff format --check .

# Type checking
mypy

# Tests
pytest
```

## Repository structure
```text
src/atlas/       Application source code
tests/           Automated tests
docs/            Architecture and engineering documentation
```

## Engineering workflow

Work is performed on short-lived feature branches. Each feature is tracked by
an issue, tested, reviewed through a pull request, and merged into `main`
when it is ready.